"""Map honeypot requests to likely CVEs based on exploit signatures.

Signatures are heuristic: a matching request indicates an attacker is probing
for or attempting to exploit a known vulnerability, not that the target is
vulnerable.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Pattern


@dataclass(frozen=True)
class CVERule:
    cve_id: str
    name: str
    product: str
    severity: str
    confidence: str  # confirmed, likely, possible
    path: Optional[Pattern] = None
    query: Optional[Pattern] = None
    body: Optional[Pattern] = None
    combined: Optional[Pattern] = None
    notes: str = ""


def _p(pattern: str) -> Pattern:
    return re.compile(pattern, re.IGNORECASE)


# Ordered rules: first match wins (most specific signatures first).
CVE_RULES: List[CVERule] = [
    CVERule(
        cve_id="CVE-2017-9841",
        name="PHPUnit eval-stdin.php remote code execution",
        product="PHPUnit",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"eval-stdin\.php"),
        notes="Exposed vendor/phpunit eval-stdin.php allows arbitrary PHP execution.",
    ),
    CVERule(
        cve_id="CVE-2025-55182",
        name="React Server Components unsafe deserialization (React2Shell)",
        product="React / Next.js",
        severity="CRITICAL",
        confidence="confirmed",
        body=_p(r"__proto__.*(?:child_process|execsync|exec\s*\()"),
        notes="Prototype pollution in React Flight protocol leads to RCE.",
    ),
    CVERule(
        cve_id="CVE-2024-34102",
        name="Adobe Commerce CosmicSting XXE (metadatauploader)",
        product="Adobe Commerce / Magento",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"metadatauploader"),
        notes="XXE via /rest/V1/guest-carts/.../payment-information or metadatauploader path.",
    ),
    CVERule(
        cve_id="CVE-2021-26855",
        name="Microsoft Exchange ProxyLogon SSRF",
        product="Microsoft Exchange Server",
        severity="CRITICAL",
        confidence="confirmed",
        combined=_p(r"autodiscover\.json.*(?:@zdi|powershell|cmd|proxylogon)"),
        notes="SSRF via Autodiscover endpoint; often chained with CVE-2021-27065.",
    ),
    CVERule(
        cve_id="CVE-2021-27065",
        name="Microsoft Exchange ProxyLogon arbitrary file write",
        product="Microsoft Exchange Server",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"ecp/Current/exporttool/microsoft\.exchange\.ediscovery\.exporttool"),
        notes="Post-auth file write; commonly paired with CVE-2021-26855.",
    ),
    CVERule(
        cve_id="CVE-2021-26855",
        name="Microsoft Exchange ProxyLogon SSRF",
        product="Microsoft Exchange Server",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"autodiscover/autodiscover\.json"),
        notes="Autodiscover probe; may be recon for ProxyLogon chain.",
    ),
    CVERule(
        cve_id="CVE-2021-3129",
        name="Laravel Ignition debug mode RCE",
        product="Laravel Ignition",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"_ignition/execute-solution"),
        notes="Unauthenticated RCE when debug mode is enabled.",
    ),
    CVERule(
        cve_id="CVE-2018-20062",
        name="ThinkPHP invokefunction RCE",
        product="ThinkPHP",
        severity="CRITICAL",
        confidence="confirmed",
        combined=_p(r"think\\app/invokefunction|invokefunction.*call_user_func"),
        notes="Remote code execution via invokefunction parameter.",
    ),
    CVERule(
        cve_id="CVE-2021-41773",
        name="Apache HTTP Server path traversal",
        product="Apache HTTP Server",
        severity="HIGH",
        confidence="confirmed",
        path=_p(r"cgi-bin/.*\.\./.*(?:bin/sh|bin/bash|etc/passwd)"),
        notes="Path traversal on Apache 2.4.49; CVE-2021-42013 extends to 2.4.50.",
    ),
    CVERule(
        cve_id="CVE-2024-3400",
        name="Palo Alto PAN-OS GlobalProtect command injection",
        product="Palo Alto PAN-OS",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"webui/"),
        notes="Pre-auth RCE via GlobalProtect gateway.",
    ),
    CVERule(
        cve_id="CVE-2024-3400",
        name="Palo Alto PAN-OS GlobalProtect command injection",
        product="Palo Alto PAN-OS",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"validate-sso/.*\.\./"),
        notes="Path traversal in SSO validation endpoint.",
    ),
    CVERule(
        cve_id="CVE-2024-36401",
        name="GeoServer OGC Filter SQL injection RCE",
        product="GeoServer",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"geoserver"),
        notes="Unauthenticated RCE via WFS/WMS filter expressions.",
    ),
    CVERule(
        cve_id="CVE-2019-19781",
        name="Citrix ADC/Gateway directory traversal",
        product="Citrix ADC / Gateway",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"(?:vpn/index\.html|vpns/|logon/logonpoint)"),
        notes="Path traversal leading to arbitrary command execution.",
    ),
    CVERule(
        cve_id="CVE-2024-53704",
        name="SonicWall SMA100 SSLVPN authentication bypass",
        product="SonicWall SMA",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"vpnsvc/connect\.cgi"),
        notes="Auth bypass on SonicWall Secure Mobile Access.",
    ),
    CVERule(
        cve_id="CVE-2019-0193",
        name="Apache Solr DataImportHandler RCE",
        product="Apache Solr",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"/solr/"),
        notes="Remote code execution via DataImportHandler.",
    ),
    CVERule(
        cve_id="CVE-2019-1003000",
        name="Jenkins script security sandbox bypass",
        product="Jenkins",
        severity="HIGH",
        confidence="likely",
        path=_p(r"(?:/jenkins/script|/script(?:/|$))"),
        notes="Groovy sandbox bypass via crafted payloads.",
    ),
    CVERule(
        cve_id="CVE-2022-22965",
        name="Spring Framework RCE (Spring4Shell)",
        product="Spring Framework",
        severity="CRITICAL",
        confidence="possible",
        combined=_p(r"class\.module\.classLoader|tomcat.*war"),
        notes="ClassLoader manipulation on JDK 9+ with Tomcat.",
    ),
    CVERule(
        cve_id="CVE-2021-44228",
        name="Apache Log4j JNDI injection (Log4Shell)",
        product="Apache Log4j",
        severity="CRITICAL",
        confidence="confirmed",
        combined=_p(r"\$\{jndi:(?:ldap|rmi|dns)://"),
        notes="JNDI lookup via crafted log input.",
    ),
    CVERule(
        cve_id="CVE-2022-1388",
        name="F5 BIG-IP iControl REST authentication bypass",
        product="F5 BIG-IP",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"mgmt/tm/util/bash"),
        notes="Unauthenticated RCE via iControl REST.",
    ),
    CVERule(
        cve_id="CVE-2023-22527",
        name="Atlassian Confluence OGNL injection RCE",
        product="Atlassian Confluence",
        severity="CRITICAL",
        confidence="likely",
        combined=_p(r"confluence.*ognl|/template/aui/text-inline\.vm"),
        notes="Template injection in Confluence Server/Data Center.",
    ),
    CVERule(
        cve_id="CVE-2022-26134",
        name="Atlassian Confluence OGNL injection RCE",
        product="Atlassian Confluence",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"/\$\{.*\}/"),
        notes="OGNL injection via URI path.",
    ),
    CVERule(
        cve_id="CVE-2023-4966",
        name="Citrix Bleed information disclosure",
        product="Citrix NetScaler ADC/Gateway",
        severity="CRITICAL",
        confidence="possible",
        path=_p(r"(?:/oauth/idp|/logon/LogonPoint)"),
        notes="Sensitive memory leak from NetScaler ADC/Gateway.",
    ),
    CVERule(
        cve_id="CVE-2023-3519",
        name="Citrix ADC/Gateway unauthenticated RCE",
        product="Citrix ADC / Gateway",
        severity="CRITICAL",
        confidence="possible",
        path=_p(r"(?:/vpn/|/vpns/|/logon/)"),
        notes="Code injection on NetScaler ADC and Gateway.",
    ),
    CVERule(
        cve_id="CVE-2022-41082",
        name="Microsoft Exchange ProxyNotShell RCE",
        product="Microsoft Exchange Server",
        severity="HIGH",
        confidence="likely",
        path=_p(r"autodiscover/autodiscover\.xml"),
        notes="Post-auth RCE chain on Exchange Server 2016/2019.",
    ),
    CVERule(
        cve_id="CVE-2022-22963",
        name="Spring Cloud Function SpEL injection RCE",
        product="Spring Cloud Function",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"functionRouter"),
        notes="Routing expression injection in Spring Cloud Function.",
    ),
    CVERule(
        cve_id="CVE-2017-5638",
        name="Apache Struts2 Jakarta multipart RCE",
        product="Apache Struts",
        severity="CRITICAL",
        confidence="likely",
        combined=_p(r"content-type:.*multipart.*%\{|struts.*ognl"),
        notes="OGNL injection via Content-Type header.",
    ),
    CVERule(
        cve_id="CVE-2022-24086",
        name="Magento PEAR command injection",
        product="Adobe Commerce / Magento",
        severity="CRITICAL",
        confidence="likely",
        query=_p(r"pearcmd.*config-create"),
        notes="LFI chained to PEAR config-create for code execution.",
    ),
    CVERule(
        cve_id="CVE-2023-46604",
        name="Apache ActiveMQ OpenWire deserialization RCE",
        product="Apache ActiveMQ",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"admin/(?:queue|topic)"),
        notes="Unsafe deserialization on OpenWire protocol.",
    ),
    CVERule(
        cve_id="CVE-2023-34362",
        name="MOVEit Transfer SQL injection",
        product="Progress MOVEit Transfer",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"human\.aspx"),
        notes="SQL injection leading to remote code execution.",
    ),
    CVERule(
        cve_id="CVE-2021-26084",
        name="Atlassian Confluence OGNL injection RCE",
        product="Atlassian Confluence",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"pages/doenterpagevariables"),
        notes="OGNL injection in Confluence Server.",
    ),
    CVERule(
        cve_id="CVE-2020-1472",
        name="Netlogon elevation of privilege (Zerologon)",
        product="Microsoft Windows Netlogon",
        severity="CRITICAL",
        confidence="possible",
        path=_p(r"/Dr0v"),
        notes="Often used as a scanner fingerprint for Zerologon-related activity.",
    ),
    CVERule(
        cve_id="CVE-2023-22515",
        name="Atlassian Confluence broken access control",
        product="Atlassian Confluence",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"server-info\.action"),
        notes="Unauthenticated admin account creation.",
    ),
    CVERule(
        cve_id="CVE-2022-22947",
        name="Spring Cloud Gateway SpEL injection RCE",
        product="Spring Cloud Gateway",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"actuator/gateway/routes"),
        notes="Malicious route definition via actuator endpoint.",
    ),
    CVERule(
        cve_id="CVE-2018-7600",
        name="Drupalgeddon2 remote code execution",
        product="Drupal",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"user/register\?.*destination="),
        notes="Form API render array injection.",
    ),
    CVERule(
        cve_id="CVE-2019-6340",
        name="Drupal REST module RCE",
        product="Drupal",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"node/\?.*_format=hal_json"),
        notes="Deserialization via HAL JSON REST endpoint.",
    ),
    CVERule(
        cve_id="CVE-2023-6553",
        name="WordPress Backup Migration plugin RCE",
        product="WordPress Backup Migration",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"backup-backup/includes/backup-heart\.php"),
        notes="Unauthenticated RCE via backup-heart.php.",
    ),
    CVERule(
        cve_id="CVE-2023-6000",
        name="WordPress Popup Builder plugin XSS/RCE chain",
        product="WordPress Popup Builder",
        severity="HIGH",
        confidence="possible",
        path=_p(r"popup-builder"),
        notes="Stored XSS that can lead to admin takeover.",
    ),
    CVERule(
        cve_id="CVE-2024-27956",
        name="WordPress WP-Automatic plugin SQL injection",
        product="WordPress WP-Automatic",
        severity="CRITICAL",
        confidence="likely",
        path=_p(r"wp-automatic"),
        notes="SQL injection leading to admin access.",
    ),
    CVERule(
        cve_id="CVE-2022-21661",
        name="WordPress WP_Query SQL injection",
        product="WordPress Core",
        severity="HIGH",
        confidence="possible",
        path=_p(r"wp-json/wp/v2/posts"),
        notes="SQLi via WP_Query when plugins expose endpoints.",
    ),
]

# Generic techniques that are not tied to one CVE but worth labeling.
GENERIC_TECHNIQUES: List[CVERule] = [
    CVERule(
        cve_id="TECH-XDEBUG-RCE",
        name="Xdebug remote debugging code execution",
        product="Xdebug (misconfiguration)",
        severity="HIGH",
        confidence="likely",
        query=_p(r"xdebug_session_start"),
        notes="Remote debugging enabled; not a CVE but a common RCE vector.",
    ),
    CVERule(
        cve_id="TECH-DOCKER-API",
        name="Exposed Docker remote API",
        product="Docker",
        severity="CRITICAL",
        confidence="confirmed",
        path=_p(r"/containers/json"),
        notes="Unauthenticated container management if API is exposed.",
    ),
    CVERule(
        cve_id="TECH-SPRING-ACTUATOR",
        name="Spring Boot Actuator information disclosure",
        product="Spring Boot Actuator",
        severity="MEDIUM",
        confidence="likely",
        path=_p(r"/actuator/(?:env|heapdump|configprops|mappings|beans)"),
        notes="Sensitive env/config exposure; may enable further exploitation.",
    ),
    CVERule(
        cve_id="TECH-GIT-EXPOSURE",
        name="Exposed .git repository",
        product="Git",
        severity="HIGH",
        confidence="confirmed",
        path=_p(r"\.git/(?:config|HEAD|index)"),
        notes="Source code and secrets leak; CWE-527 rather than a single CVE.",
    ),
    CVERule(
        cve_id="TECH-ENV-EXPOSURE",
        name="Exposed environment file (.env)",
        product="Application configuration",
        severity="HIGH",
        confidence="confirmed",
        path=_p(r"(?:^|/)\.env(?:\.|$|[\w.-])"),
        notes="Credential and API key disclosure; CWE-200.",
    ),
    CVERule(
        cve_id="TECH-WP-XMLRPC",
        name="WordPress XML-RPC brute force / amplification",
        product="WordPress",
        severity="MEDIUM",
        confidence="likely",
        path=_p(r"xmlrpc\.php"),
        notes="Brute force and pingback amplification; not one specific CVE.",
    ),
]

ALL_RULES = CVE_RULES + GENERIC_TECHNIQUES

_CONFIDENCE_ORDER = {"confirmed": 0, "likely": 1, "possible": 2}


def _path(req: dict) -> str:
    return (req.get("path") or req.get("url") or "").lower()


def _query(req: dict) -> str:
    return (req.get("query") or "").lower()


def _body(req: dict) -> str:
    return req.get("body") or ""


def _combined(req: dict) -> str:
    return " ".join((_path(req), _query(req), _body(req)))


def _rule_matches(rule: CVERule, req: dict) -> bool:
    path = _path(req)
    query = _query(req)
    body = _body(req)
    combined = _combined(req)

    if rule.path and not rule.path.search(path):
        return False
    if rule.query and not rule.query.search(query):
        return False
    if rule.body and not rule.body.search(body):
        return False
    if rule.combined and not rule.combined.search(combined):
        return False
    return bool(rule.path or rule.query or rule.body or rule.combined)


def _rule_to_dict(rule: CVERule) -> Dict[str, str]:
    return {
        "cve_id": rule.cve_id,
        "name": rule.name,
        "product": rule.product,
        "severity": rule.severity,
        "confidence": rule.confidence,
        "notes": rule.notes,
    }


def identify_cves(req: dict, include_generic: bool = True) -> List[Dict[str, str]]:
    """Return all matching CVE/technique labels for a request, best match first."""
    rules = ALL_RULES if include_generic else CVE_RULES
    seen_ids = set()
    matches: List[Dict[str, str]] = []

    for rule in rules:
        if rule.cve_id in seen_ids:
            continue
        if _rule_matches(rule, req):
            seen_ids.add(rule.cve_id)
            matches.append(_rule_to_dict(rule))

    matches.sort(key=lambda m: _CONFIDENCE_ORDER.get(m["confidence"], 9))
    return matches


def primary_cve(req: dict, include_generic: bool = True) -> Optional[Dict[str, str]]:
    """Return the highest-confidence CVE match for a request, if any."""
    matches = identify_cves(req, include_generic=include_generic)
    return matches[0] if matches else None


def get_cve_catalog() -> List[Dict[str, str]]:
    """Return the full CVE/technique rule catalog for documentation."""
    catalog = []
    seen = set()
    for rule in ALL_RULES:
        if rule.cve_id in seen:
            continue
        seen.add(rule.cve_id)
        catalog.append(_rule_to_dict(rule))
    return catalog


def get_cve_info(cve_id: str) -> Optional[Dict[str, str]]:
    """Return catalog metadata for a CVE/technique ID, if known."""
    needle = cve_id.upper()
    for entry in get_cve_catalog():
        if entry["cve_id"].upper() == needle:
            return entry
    return None


def resolve_cve_id(name: str) -> Optional[str]:
    """Resolve a CVE or technique ID case-insensitively."""
    catalog = get_cve_catalog()
    upper = name.upper()
    for entry in catalog:
        if entry["cve_id"].upper() == upper:
            return entry["cve_id"]
    return None


def request_matches_cve(req: dict, cve_id: str, include_generic: bool = True) -> bool:
    """Return True if the request matches the given CVE/technique signature."""
    needle = cve_id.upper()
    return any(m["cve_id"].upper() == needle for m in identify_cves(req, include_generic=include_generic))
