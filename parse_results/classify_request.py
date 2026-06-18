"""Content-based attack classification for honeypot request logs.

Derives attack type from path, query, headers, and body instead of relying on
the log's pre-assigned classification field, which is often incorrect.
"""

import re
from typing import Dict, Optional

CLASSIFICATION_LABELS: Dict[str, str] = {
    "rce_attempt": "Remote code execution (RCE) attempt",
    "crypto_mining_probe": "Cryptocurrency mining RPC probe",
    "dns_probe": "DNS-over-HTTPS / DNS tunnel probe",
    "path_traversal_attempt": "Path traversal attempt",
    "sensitive_file_probe": "Sensitive file probing (.env, .git, config)",
    "citrix_vpn_probe": "VPN / network appliance probing",
    "wordpress_plugin_probe": "WordPress plugin vulnerability probing",
    "login_attempt": "Login / credential attack",
    "wordpress_probe": "WordPress vulnerability probing",
    "webdav_probe": "WebDAV scanning (PROPFIND)",
    "reconnaissance": "Benign discovery / page-load traffic",
    "unknown": "Unclassified / other",
}

CLASSIFICATION_DESCRIPTIONS: Dict[str, str] = {
    "rce_attempt": (
        "Attempts to achieve remote code execution via exploit payloads such as "
        "React Server Components prototype pollution, PHPUnit eval-stdin, Xdebug "
        "session probes, command injection, Exchange ProxyLogon, Jenkins console, "
        "or shell invocation — not routine WordPress admin/setup pages."
    ),
    "crypto_mining_probe": (
        "Probes for exposed cryptocurrency mining JSON-RPC endpoints "
        "(getwork, eth_getWork, mining.subscribe)."
    ),
    "dns_probe": (
        "DNS-over-HTTPS or DNS tunnel measurement probes using application/dns-message "
        "content or encoded DNS queries on common DoH paths."
    ),
    "path_traversal_attempt": (
        "Attempts to escape the web root using ../ sequences, often targeting "
        "CGI binaries like /bin/sh for remote code execution."
    ),
    "sensitive_file_probe": (
        "Attempts to retrieve sensitive configuration files such as .env, .git/config, "
        "CI/CD secrets, cloud credentials, terraform vars, and database dumps."
    ),
    "citrix_vpn_probe": (
        "Scans for VPN gateways, firewalls, and network appliances: Citrix, SonicWall, "
        "SSL VPN, WebUI login pages, Geoserver, ONVIF, MikroTik, and similar services."
    ),
    "wordpress_plugin_probe": (
        "Probes for vulnerable WordPress plugin PHP endpoints, readme files, and "
        "admin paths — not plugin CSS/JS/font assets loaded by the browser."
    ),
    "login_attempt": (
        "Credential attacks and login-page discovery: brute-force attempts, admin "
        "panel login URLs, WordPress/cPanel/OWA logins, and showLogin-style probes."
    ),
    "wordpress_probe": (
        "Unauthenticated scans of WordPress attack surfaces: wp-login.php, xmlrpc.php, "
        "wp-json REST API, wp-admin PHP endpoints, and theme/plugin PHP files — not "
        "authenticated admin sessions or honeypot operator traffic."
    ),
    "reconnaissance": (
        "Benign or operational traffic: root page views, favicon/robots.txt, WordPress "
        "static assets, authenticated admin sessions, and honeypot setup activity."
    ),
    "webdav_probe": (
        "WebDAV scanning using PROPFIND or OPTIONS to discover directories, "
        "often preceding exploitation of misconfigured servers."
    ),
    "unknown": "Requests that did not match a specific attack signature.",
}

SEVERITY: Dict[str, str] = {
    "rce_attempt": "HIGH",
    "path_traversal_attempt": "HIGH",
    "login_attempt": "HIGH",
    "crypto_mining_probe": "MEDIUM",
    "sensitive_file_probe": "MEDIUM",
    "citrix_vpn_probe": "MEDIUM",
    "wordpress_plugin_probe": "MEDIUM",
    "wordpress_probe": "MEDIUM",
    "dns_probe": "LOW",
    "webdav_probe": "LOW",
    "reconnaissance": "LOW",
    "unknown": "LOW",
}

# Honeypot operator / lab traffic — excluded from attack counts.
OPERATOR_IPS = frozenset({"86.85.100.18"})

# Ordered rules: first match wins (most specific patterns first).
# /etc/passwd is intentionally omitted: bare passwd reads are sensitive_file_probe
# or path_traversal_attempt; only requests with other exploit indicators stay RCE.
_RCE_BODY_PATTERNS = re.compile(
    r"(?:__proto__|child_process|execsync|exec\s*\(|/bin/sh|/bin/bash|"
    r"powershell|cmd\.exe|wget\s+http|curl\s+http|process\.mainmodule|"
    r"base64_decode|passthru\s*\(|system\s*\(|shell_exec|"
    r"proxylogon|autodiscover\.json|eval\s*\(|invoke-expression|"
    r"<\?php|<\?=|phpinfo\s*\(|md5\s*\(\s*[\"']phpunit|md5\s*\(\s*[\"']Hello)",
    re.IGNORECASE,
)
_RCE_QUERY = re.compile(
    r"(?:xdebug|phpstorm|allow_url_include|auto_prepend_file|"
    r"php://input|expect://|data://text/plain|invokefunction|think\\app|pearcmd)",
    re.IGNORECASE,
)
_RCE_PATH = re.compile(
    r"(?:"
    r"eval-stdin\.php|"
    r"phpunit/|"
    r"thinkphp|"
    r"invokefunction|"
    r"pearcmd|"
    r"(?:/|^)(?:shell|cmd|backdoor|webshell)\.php|"
    r"metadatauploader|"
    r"/jenkins/script|"
    r"/console(?:/|$)|"
    r"/solr/|"
    r"exchange\.ediscovery\.exporttool|"
    r"/_ignition/execute-solution|"
    r"/adminer(?:/|\.php|$)|"
    r"/ReportServer|"
    r"/containers/json|"
    r"/restore\.php|"
    r"/dump\.php|"
    r"/upload\.php|"
    r"/import\.php|"
    r"/migrate\.php|"
    r"/repair\.php|"
    r"/upgrade\.php|"
    r"/backup\.php|"
    r"/export\.php|"
    r"/cron\.php|"
    r"/file\.php|"
    r"/download\.php|"
    r"alive\.php"
    r")",
    re.IGNORECASE,
)
_MINING_BODY_PATTERNS = re.compile(
    r'"(?:method|params)"\s*:\s*"(?:getwork|get_work|eth_getwork|eth_submitwork|'
    r'mining\.subscribe|mining\.authorize|xmr\.|stratum)',
    re.IGNORECASE,
)
_MINING_SIMPLE = re.compile(
    r"\b(?:getwork|eth_getwork|eth_submitwork|mining\.subscribe)\b",
    re.IGNORECASE,
)
_PATH_TRAVERSAL = re.compile(
    r"(?:\.\./|%2e%2e|%2e%2e/|\.\.%2f|%2e%2e%2f|\.\.\\|%2e%2e%5c|%5c%2e%2e)",
    re.IGNORECASE,
)

# Sensitive-file heuristics: extensions, path keywords, and known config filenames.
_SENSITIVE_EXTENSIONS = re.compile(
    r"\.(?:"
    r"env(?:\.[\w-]+)?|ya?ml|json|properties|toml|ini|cfg|conf|xml|sql|sqlite3?|db|"
    r"pem|key|pfx|p12|ppk|jks|crt|cert|log|bak|old|swp|save|txt|csv|zip|gz|tar|"
    r"map|hcl|sls|plist|tfvars|lock|sum|cnf|rc|history|profile|passwd|shadow|"
    r"envrc|tfstate|enc|hgrc|manifest|prisma|gradle|cf|bakup|temp|tmp|settings|"
    r"override|sample|inc|local|prod|staging|dev|test|production|development|"
    r"backup|copy|bz2|tfvars|tfstate|dockerfile|"
    r"properties|toml|ini|yaml|yml|json|xml|sql|log|hcl|sls|plist|ppk|p12|"
    r"pfx|crt|cert|db|sqlite|lock|sum|cfg|conf|cnf|rc|enc|hgrc|manifest|prisma"
    r")(?:$|\?)",
    re.IGNORECASE,
)
_SENSITIVE_KEYWORDS = re.compile(
    r"(?:"
    r"secrets?|credentials?|credential|creds?|tokens?|apikeys?|api-keys?|api_keys?|"
    r"passwords?|passwd|private[_-]?key|id_rsa|id_dsa|id_ed25519|id_ecdsa|"
    r"service[_-]?account|jwt|refresh_token|access_token|usersecrets|"
    r"wp-config|web\.config|app\.config|appsettings|application[-_]?(?:prod|dev|local|test)|"
    r"bootstrap|database|docker-compose|dockerfile|compose\.|Dockerfile|"
    r"terraform|kubernetes|k8s|helm|vault|jenkins|(?:^|/)adminer(?:/|\.php|$)|phpinfo|_phpinfo|"
    r"ignition|actuator|kubeconfig|kube-config|"
    r"github-actions|gitlab-ci|azure-pipelines|bitbucket-pipelines|buildkite|travis|"
    r"drone|buildspec|serverless|amplify|pulumi|cloudbuild|helmfile|skaffold|"
    r"render|railway|fly|wrangler|netlify|vercel|heroku|amplify|samconfig|cdk|"
    r"pipeline|workflows?|build\.|deploy\.|release\.|"
    r"\.env|\.git|\.aws|\.ssh|\.azure|\.gcp|\.kube|\.terraform|\.docker|\.firebase|"
    r"\.vercel|\.netlify|\.cargo|\.gem|\.m2|\.gradle|\.idea|\.npmrc|\.yarnrc|"
    r"\.s3cfg|\.netrc|\.boto|\.pypirc|\.dotenv|\.secrets|\.secret|\.ftpconfig|"
    r"\.vault|\.mysql_history|\.psql_history|\.bash_history|\.bash_profile|"
    r"\.bash_logout|\.profile|\.passwd|\.hg/|\.capistrano|\.travis|\.drone|"
    r"\.semaphore|\.buildkite|\.woodpecker|\.wrangler|\.config|\.gist|\.shopify|"
    r"\.sqlite_history|\.mwsql_history|\.mongooserc|\.kubeconfig|\.terraformrc|"
    r"nginx\.conf|Caddyfile|connectionStrings|launchSettings|"
    r"next\.config|nuxt\.config|gatsby-config|pm2\.config|firebase|google-services|"
    r"stripe|sentry|newrelic|grafana|prometheus|keycloak|consul|datadog|"
    r"traefik|rabbitmq|airflow|celery|gunicorn|superset|directus|hasura|prisma|"
    r"ormconfig|knexfile|shopify|supabase|dynatrace|splunk|kibana|logstash|"
    r"alertmanager|telegraf|nats|composer\.auth|ftpconfig|sftp-config|"
    r"deployment_config|deploy-config|server-config|server_config|app-config|"
    r"appConfig|global\.(?:json|ya?ml|env)|"
    r"manage/(?:health|info|beans|configprops|env|heapdump|logfile|metrics|trace)|"
    r"WEB-INF|META-INF|/config(?:/|$|\.)|/settings(?:/|$|\.)|/secrets(?:/|$|\.)|"
    r"/credentials(?:/|$|\.)|/env(?:/|$|\.)|/database(?:/|$|\.)|"
    r"local_settings|settings\.php|configuration\.php|database\.php|db\.php|connect\.php|"
    r"heapdump|debug\.log|error\.log|access\.log|laravel\.log|production\.log|"
    r"wp-debug|wp-content/debug|storage/logs|/logs/|/var/log/|"
    r"schema\.sql|backup\.(?:sql|tar|zip|gz)|dump\.(?:sql|php)|"
    r"master\.passwd|/shadow|/passwd(?:\.txt|$)|"
    r"aws[_-]?credentials|gcp[_-]?credentials|azure[_-]?credentials|"
    r"google-credentials|service-account|iam_credentials|ec2_credentials|"
    r"s3_credentials|keys\.(?:json|txt)|secret[_-]?key|secretkey|"
    r"mysql\.env|postgres\.env|redis\.env|mongodb\.env|database\.env|db\.env|"
    r"stripe\.env|heroku\.env|gradle\.env|maven\.env|go\.env|ant\.env|"
    r"Copy of \.env|env_copy|env\.(?:bak|old|backup|local|prod|staging|dev|test|txt|json|yaml|zip|gz|tar)|"
    r"secrets\.env|credentials\.env|database\.env|"
    r"pip\.ini|pip\.conf|NuGet\.Config|nuget\.config|settings\.xml|"
    r"requirements(?:-dev)?\.txt|Gemfile|composer\.|package-lock|yarn\.lock|"
    r"pnpm-lock|Pipfile|poetry\.lock|poetry\.toml|Cargo\.toml|go\.sum|pom\.xml|"
    r"Makefile|Procfile|Vagrantfile|Jenkinsfile|build\.gradle|gradle\.properties|"
    r"appspec\.yml|buildspec\.yml|cloudbuild\.yaml|skaffold\.yaml|helmfile\.yaml|"
    r"inventory\.yml|ansible\.cfg|terraform/|pulumi\.|cdk\.json|serverless\.|"
    r"arm_template|deployment\.json|deploy\.json|ftp-deploy|"
    r"1password|passwords\.json|accounts\.txt|users\.txt|logins\.txt|userpass|"
    r"pass\.txt|passwd\.txt|creds\.|/creds(?:/|$|\.)|"
    r"users\.db|data\.db|app\.db|main\.db|prod\.db|production\.db|local\.db|"
    r"users\.sqlite|db\.sqlite|db1\.sqlite|data\.sqlite|db\.sqlite3|"
    r"backup\.tar|env\.tar|secrets\.tar|config\.tar|config\.zip|credentials\.zip|"
    r"backup\.zip|secrets\.zip|env\.zip|"
    r"client\.(?:crt|key)|server\.(?:crt|key|cert|pem|pfx)|ca\.(?:crt|pem|key)|"
    r"private\.pem|public_key\.pem|certificate\.pfx|keystore\.|rootCA\.|"
    r"ssl/|/certs/|/cert/|"
    r"CVS/|/inventory$|/inventory/|salt/pillar|chef/|ansible/|playbooks/|"
    r"group_vars|host_vars|manifests/|charts/|infra/|ops/|cluster/|"
    r"tekton/|skaffold|wrangler\.toml|fly\.toml|railway\.toml|netlify\.toml|"
    r"render\.yaml|appsettings\.|Properties/|target/classes/|build/resources/|"
    r"src/main/resources/|src/config|backend/config|api/config|conf/|instance/|"
    r"mysite/|myapp/|project/settings|core/settings|settings/(?:production|local|dev|base)|"
    r"django/settings|laravel/config|laravel/storage|magento/|joomla/|drupal/|"
    r"sites/default/|administrator/configuration|"
    r"\.next/static|\.js\.map|\.chunk\.js\.map|bundle\.js\.map|main\.js\.map|"
    r"asset-manifest|app\.js\.map|"
    r"local\.py|configuration\.py|secrets\.py|settings\.py|config\.py|credentials\.py|"
    r"seeds\.rb|schema\.rb|deploy\.rb|env\.rb|"
    r"variables\.tf|outputs\.tf|main\.tf|"
    r"(?:^|/)(?:setup|install|init|cron|cronjob|run|start|deploy|test|script|bootstrap)\.sh|"
    r"(?:^|/)test\.(?:rb|js|py)$|"
    r"mongooserc|\.bazelrc|"
    r"/\.(?:_env|~env)|^/\.$|"
    r"nginx/sites-available|/messages$|/syslog$|"
    r"themes/\.env|includes/\.env|wp-admin/\.env|wp-includes/\.env|plugins/\.env"
    r")",
    re.IGNORECASE,
)
_SENSITIVE_PHP = re.compile(
    r"/(?:settings|config|database|db|connect|connection|adminer|phpinfo|info|test|debug|"
    r"wp-config|(?:^|/)install\.php|setup|restore|dump|upload|backup|export|import|migrate|repair|"
    r"upgrade|cron|function|global|common|localsettings|"
    r"configuration|credentials|secrets|passwd|passwords|setting|dbconn|"
    r"includes/(?:db|database|connect|connection|settings)|"
    r"inc/(?:db|database)|lib/(?:db|database)|application/config|"
    r"administrator|wp-settings|configuration|database_config|db_config|"
    r"config_(?:local|dev|prod|test|staging)|config\d|config_local|config_dev|"
    r"config_prod|local\.php|global\.php|common\.php|connection\.php|"
    r"dump|restore|repair|upgrade|migrate|export|import|backup|upload|download|"
    r"file|setup|test|debug|info)\.php",
    re.IGNORECASE,
)
_NOT_SENSITIVE = re.compile(
    r"(?:wp-login\.php|/wp-admin(?:/[^/]+)*\.php$|showlogin|^/admin/?$|"
    r"wp-json|xmlrpc\.php|wp-cron\.php|"
    r"wp-includes/(?:css|js|images|fonts)/|wp-admin/(?:css|js|images|fonts)/|"
    r"wp-content/themes/[^/]+\.(?:css|js|woff|png|jpg|gif|svg|ico)|"
    r"wp-content/plugins/[^/]+/.+\.(?:css|js|woff|png|jpg|gif|svg|ico))",
    re.IGNORECASE,
)
_SENSITIVE_PATH = re.compile(
    r"(?:"
    r"(?:^|/)\.env[\w.-]*|"
    r"(?:^|/)\.git[\w.-]*|"
    r"^/\.git/|"
    r"^/\.aws/|"
    r"(?:^|/)\.(?:htpasswd|htaccess|svn|DS_Store|npmrc|boto|pypirc|envrc)(?:/|$|\.)|"
    r"(?:^|/)\.cargo/credentials|"
    r"(?:^|/)\.github/|"
    r"(?:^|/)\.gitlab[\w.-]*|"
    r"(?:^|/)\.ssh/|"
    r"wp-config|"
    r"(?:^|/)aws\.(?:env|yaml|credentials)|"
    r"(?:^|/)auth\.(?:json|log)|"
    r"(?:^|/)secrets\.|"
    r"(?:^|/)terraform\.|"
    r"(?:^|/)docker-compose|"
    r"(?:^|/)Jenkinsfile|"
    r"(?:^|/)circle\.yml|"
    r"(?:^|/)pip\.ini|"
    r"(?:^|/)pyproject\.toml|"
    r"(?:^|/)ecosystem\.config|"
    r"(?:^|/)composer\.|"
    r"(?:^|/)package\.json|"
    r"(?:^|/)config\.|"
    r"(?:^|/)config/|"
    r"(?:^|/)parameters\.yml|"
    r"(?:^|/)dump\.sql|"
    r"(?:^|/)backup\.|"
    r"(?:^|/)database\.|"
    r"(?:^|/)env$|"
    r"(?:^|/)~/.composer/auth\.json|"
    r"(?:^|/)aws_credentials|"
    r"(?:^|/)token|"
    r"(?:^|/)application\.|"
    r"(?:^|/)terraform\.tfstate|"
    r"(?:^|/)\.netrc|"
    r"(?:^|/)pip\.conf|"
    r"(?:^|/)\.pip/|"
    r"(?:^|/)boto\.cfg|"
    r"(?:^|/)package-lock|"
    r"(?:^|/)Pipfile|"
    r"(?:^|/)bitbucket-pipelines|"
    r"(?:^|/)yarn\.lock|"
    r"(?:^|/)build\.gradle|"
    r"(?:^|/)\.dotenv|"
    r"(?:^|/)\.terraform/|"
    r"^/phpinfo\.php|"
    r"^/server-status|"
    r"^/\.well-known/security\.txt|"
    r"/actuator(?:/|$)|"
    r"/_ignition/|"
    r"/adminer|"
    r"/manage/|"
    r"/heapdump|"
    r"/WEB-INF/|"
    r"/META-INF/"
    r")",
    re.IGNORECASE,
)
_CITRIX_PATH = re.compile(
    r"(?:"
    r"vpn/index\.html|"
    r"logon/logonpoint|"
    r"vpns/|"
    r"citrix/|"
    r"nf/auth|"
    r"vpnsvc/connect\.cgi|"
    r"sonicos/|"
    r"is-sslvpn-enabled|"
    r"/webui/?$|"
    r"geoserver|"
    r"onvif/|"
    r"/mcp(?:/|$)|"
    r"/Dr0v|"
    r"/ab2[gh]|"
    r"/HNAP1|"
    r"/evox/|"
    r"^/version$|"
    r"^/sdk$|"
    r"^/status$|"
    r"^/debug$|"
    r"^/sse$|"
    r"^/wiki$|"
    r"^/manage(?:/|$)|"
    r"^/actuator$|"
    r"^/server-info$"
    r")",
    re.IGNORECASE,
)
_WP_PLUGIN_STATIC_ASSET = re.compile(
    r"(?:"
    r"/wp-content/plugins/[^/]+/.+\.(?:css|js|min\.css|min\.js|woff2?|ttf|eot|"
    r"png|jpe?g|gif|webp|svg|ico|map)(?:\?|$)|"
    r"/wp-content/plugins/[^/]+/(?:css|js|images|fonts|assets|dist|build|gutenberg)/"
    r")",
    re.IGNORECASE,
)
_WP_PLUGIN_PROBE_PATH = re.compile(
    r"(?:"
    r"/wp-content/plugins/[^/]+/.+\.php|"
    r"/wp-content/plugins/[^/]+/readme\.txt|"
    r"/wp-content/plugins/[^/]+/changelog\.txt|"
    r"/wp-content/plugins/[^/]+/license\.txt|"
    r"/wp-content/plugins/[^/]+/composer\.json|"
    r"/wp-content/plugins/[^/]+/package\.json|"
    r"/wp-content/plugins/[^/]+/(?:admin|includes|public|ajax)/"
    r")",
    re.IGNORECASE,
)
_WP_STATIC_ASSET = re.compile(
    r"(?:"
    r"/wp-includes/(?:css|js|images|fonts)/|"
    r"/wp-includes/js/thickbox/|"
    r"/wp-admin/(?:css|js|images|fonts)/|"
    r"/wp-content/themes/[^/]+/.+\.(?:css|js|woff2?|ttf|eot|png|jpe?g|gif|webp|svg|ico)|"
    r"/wp-content/uploads/.+\.(?:css|js|woff2?|ttf|eot|png|jpe?g|gif|webp|svg|ico)|"
    r"/wp-includes/.+\.(?:css|js|min\.css|min\.js|woff2?|ttf|eot|png|jpe?g|gif|webp|svg|ico)(?:\?|$)"
    r")",
    re.IGNORECASE,
)
# Normal wp-admin PHP used during install, plugin setup, and day-to-day administration.
_WP_ADMIN_OPERATIONAL = re.compile(
    r"/wp-admin/(?:"
    r"admin\.php|"
    r"install\.php|"
    r"update\.php|"
    r"upload\.php|"
    r"plugin-install\.php|"
    r"async-upload\.php|"
    r"media-new\.php|"
    r"themes\.php|"
    r"plugins\.php|"
    r"options-general\.php|"
    r"users\.php|"
    r"edit\.php|"
    r"post-new\.php|"
    r"index\.php"
    r")(?:\?|$)",
    re.IGNORECASE,
)
_WP_PROBE_PATH = re.compile(
    r"(?:"
    r"/wp-login\.php|"
    r"/xmlrpc\.php|"
    r"/wp-json(?:/|$)|"
    r"/wp-cron\.php|"
    r"/wp-content/.+\.php|"
    r"/wp-includes/.+\.php|"
    r"/wp-admin/install\.php/"
    r")",
    re.IGNORECASE,
)
_LOGIN_PATH = re.compile(
    r"(?:"
    r"wp-login\.php|"
    r"wp-admin/?$|"
    r"/login(?:/|$|\?|\.(?:html|jsp|cc|do|action))|"
    r"showlogin|"
    r"logon\.aspx|"
    r"proxy_subdomain_whm/login|"
    r"/owa/auth/|"
    r"/admin/login|"
    r"/user/login|"
    r"/remote/login|"
    r"/auth/login|"
    r"/manager/html|"
    r"^/admin/?$|"
    r"signin|sign-in"
    r")",
    re.IGNORECASE,
)
_LOGIN_BODY = re.compile(
    r"(?:^|[&\s])(?:log|pwd|pass|password|user|username|admin_password|"
    r"admin_password2|wp-submit|Submit)=|"
    r"weblog_title=.*admin_password",
    re.IGNORECASE,
)
_DNS_PATH = re.compile(r"^/(?:dns-query|resolve)(?:/|$)", re.IGNORECASE)
_DNS_QUERY_PARAM = re.compile(r"(?:^|[?&])(?:dns=|name=[^&]*odns|name=[^&]*dnsmeasure)", re.IGNORECASE)
_DNS_BODY = re.compile(r"odns|dnsmeasure", re.IGNORECASE)
_RECON_PATH = re.compile(
    r"^/(?:$|favicon\.ico|robots\.txt|sitemap\.xml|sitemap_index\.xml|security\.txt)$",
    re.IGNORECASE,
)
_SCANNER_PATH = re.compile(
    r"(?:"
    r"^\*$|"
    r"^/nmaplowercheck\d+|"
    r"^/[A-Za-z0-9]{1,6}$|"
    r"^/download/file\.ext$|"
    r"^/SiteLoader$|"
    r"^/mPlayer$|"
    r"^/WuEL$|"
    r"^/teorema505$|"
    r"^/book-appointment$|"
    r"^/AGENTS\.md$|"
    r"^/[A-Za-z0-9]{8,}$"
    r")",
    re.IGNORECASE,
)
_WP_DISCOVERY = re.compile(
    r"(?:public/index\.php)",
    re.IGNORECASE,
)


def _header(req: dict, name: str) -> str:
    headers = req.get("headers") or {}
    for key, value in headers.items():
        if key.lower() == name.lower():
            return value or ""
    return ""


def _client_ip(req: dict) -> str:
    return (req.get("client_ip") or "").strip()


def _has_wp_auth_session(req: dict) -> bool:
    cookie = _header(req, "cookie")
    return "wordpress_logged_in" in cookie or bool(re.search(r"wp-settings-\d+", cookie))


def _is_authenticated_wp_admin(req: dict) -> bool:
    """True when the request carries a WP login cookie for admin/API work."""
    if not _has_wp_auth_session(req):
        return False
    path = _path(req)
    query = _query(req)
    if path.startswith("/wp-admin/") or path.rstrip("/") == "/wp-admin":
        return True
    if path == "/index.php" and "rest_route" in query:
        return True
    return False


def _is_operational_wp_admin(req: dict) -> bool:
    """Routine wp-admin pages during setup or an authenticated admin session."""
    path = _path(req)
    if not _WP_ADMIN_OPERATIONAL.search(path):
        return False
    if _has_wp_auth_session(req):
        return True
    if re.search(r"/wp-admin/install\.php(?:\?|$)", path, re.I) and _method(req) == "POST":
        return True
    return False


def _path(req: dict) -> str:
    return (req.get("path") or req.get("url") or "").lower()


def _query(req: dict) -> str:
    return (req.get("query") or "").lower()


def _body(req: dict) -> str:
    return req.get("body") or ""


def _method(req: dict) -> str:
    return (req.get("method") or "").upper()


def _combined(req: dict) -> str:
    return " ".join((_path(req), _query(req), _body(req)))


def _is_sensitive_path(path: str) -> bool:
    """Return True when a path looks like sensitive file or config probing."""
    if not path or path in ("/", "*"):
        return False
    if _NOT_SENSITIVE.search(path):
        return False
    if _SENSITIVE_PATH.search(path):
        return True
    if _SENSITIVE_KEYWORDS.search(path):
        return True
    if _SENSITIVE_PHP.search(path):
        return True
    if _SENSITIVE_EXTENSIONS.search(path):
        return True
    return False


def classify_request(req: dict) -> str:
    """Classify a honeypot request from its observable content."""
    raw_path = (req.get("path") or "").strip()
    if not raw_path:
        return "reconnaissance"

    path = _path(req)
    query = _query(req)
    body = _body(req)
    method = _method(req)
    content_type = _header(req, "content-type").lower()
    combined = _combined(req)

    if _client_ip(req) in OPERATOR_IPS:
        return "reconnaissance"

    if _MINING_BODY_PATTERNS.search(body) or _MINING_SIMPLE.search(body):
        return "crypto_mining_probe"

    if (
        "application/dns-message" in content_type
        or _DNS_PATH.match(path)
        or _DNS_QUERY_PARAM.search(query)
        or (path in ("/query", "/resolve") and _DNS_BODY.search(query + body))
        or (path == "/" and ("dns=" in query or _DNS_BODY.search(body + query)))
        or _DNS_BODY.search(body)
    ):
        return "dns_probe"

    if (
        _RCE_BODY_PATTERNS.search(combined)
        or (
            _RCE_PATH.search(path)
            and not path.lower().startswith("/wp-admin/")
        )
        or _RCE_QUERY.search(query)
        or (method == "POST" and "autodiscover" in path)
    ):
        return "rce_attempt"

    if _PATH_TRAVERSAL.search(path) or _PATH_TRAVERSAL.search(query):
        return "path_traversal_attempt"

    if _CITRIX_PATH.search(path):
        return "citrix_vpn_probe"

    if _WP_PLUGIN_STATIC_ASSET.search(path):
        return "reconnaissance"

    if _WP_PLUGIN_PROBE_PATH.search(path):
        return "wordpress_plugin_probe"

    if _LOGIN_PATH.search(path):
        if (
            method == "POST"
            or _LOGIN_BODY.search(body)
            or "logon" in path
            or "owa/auth" in path
            or "/login" in path
            or "showlogin" in path
            or path.rstrip("/") == "/admin"
            or path.rstrip("/").endswith("wp-admin")
        ):
            return "login_attempt"

    if _WP_STATIC_ASSET.search(path):
        return "reconnaissance"

    if _is_authenticated_wp_admin(req) and not _RCE_BODY_PATTERNS.search(combined):
        return "reconnaissance"

    if _is_operational_wp_admin(req) and not _RCE_BODY_PATTERNS.search(combined):
        return "reconnaissance"

    if re.search(r"/wp-admin/install\.php/", path, re.IGNORECASE):
        return "wordpress_probe"

    if _is_sensitive_path(path):
        return "sensitive_file_probe"

    if _WP_PROBE_PATH.search(path):
        return "wordpress_probe"

    if path.startswith("/wp-admin/") and path.endswith(".php"):
        return "wordpress_probe"

    if path.rstrip("/").endswith("/wp-admin"):
        return "wordpress_probe"

    if path == "/index.php" and "rest_route" in query:
        return "wordpress_probe"

    if _WP_DISCOVERY.search(path):
        return "wordpress_probe"

    if method == "PROPFIND" or (method == "OPTIONS" and path == "*"):
        return "webdav_probe"

    if _SCANNER_PATH.match(path):
        return "reconnaissance"

    if method in ("GET", "HEAD") and _RECON_PATH.match(path):
        return "reconnaissance"

    if method in ("GET", "HEAD") and path in ("/", "/favicon.ico", "/robots.txt"):
        return "reconnaissance"

    if method in ("GET", "HEAD", "POST") and path == "/":
        return "reconnaissance"

    return "unknown"


def get_classification(req: dict) -> str:
    """Return derived classification for a request record."""
    return classify_request(req)


def resolve_classification(name: str) -> Optional[str]:
    """Resolve a classification name case-insensitively, including label substrings."""
    if name in CLASSIFICATION_LABELS:
        return name
    lower = name.lower().replace(" ", "_").replace("-", "_")
    if lower in CLASSIFICATION_LABELS:
        return lower
    aliases = {
        "rce": "rce_attempt",
        "command_injection": "rce_attempt",
        "command_injection_probe": "rce_attempt",
        "crypto_mining": "crypto_mining_probe",
        "mining_probe": "crypto_mining_probe",
        "dns": "dns_probe",
        "wordpress_plugins": "wordpress_plugin_probe",
        "wordpress_plugin": "wordpress_plugin_probe",
        "citrix": "citrix_vpn_probe",
        "vpn_probe": "citrix_vpn_probe",
        "webdav": "webdav_probe",
    }
    if lower in aliases:
        return aliases[lower]
    for cls, label in CLASSIFICATION_LABELS.items():
        if lower in cls or lower in label.lower().replace(" ", "_"):
            return cls
    return None
