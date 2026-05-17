#!/bin/bash

echo "🔧 Force fixing WordPress URL..."

# 1. Directly edit wp-config.php with forced settings
sudo tee -a /var/www/html/wordpress/wp-config.php > /dev/null <<'EOF'

// FORCE PROXY URL - Override everything
define('WP_HOME', 'https://192.168.100.20/wordpress');
define('WP_SITEURL', 'https://192.168.100.20/wordpress');
define('FORCE_SSL_ADMIN', true);
define('FORCE_SSL_LOGIN', true);

// Fix for proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
$_SERVER['HTTP_HOST'] = '192.168.100.20';
$_SERVER['SERVER_NAME'] = '192.168.100.20';
EOF

# 2. Update database directly with mysql (force it)
sudo mysql -u root -p wordpress <<EOF
UPDATE wp_options SET option_value = 'https://192.168.100.20/wordpress' WHERE option_name = 'siteurl';
UPDATE wp_options SET option_value = 'https://192.168.100.20/wordpress' WHERE option_name = 'home';
DELETE FROM wp_options WHERE option_name = 'rewrite_rules';
DELETE FROM wp_options WHERE option_name LIKE '%transient%';
DELETE FROM wp_options WHERE option_name LIKE '%redirect%';
EOF

# 3. Create .htaccess to prevent redirects
sudo tee /var/www/html/wordpress/.htaccess > /dev/null <<'EOF'
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /wordpress/

# Force proxy URL and prevent redirect to backend IP
RewriteCond %{HTTP_HOST} ^192\.168\.100\.10$ [NC,OR]
RewriteCond %{HTTP_HOST} ^localhost$ [NC]
RewriteRule (.*) https://192.168.100.20/wordpress/$1 [L,R=301]

# Standard WordPress rules
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /wordpress/index.php [L]
</IfModule>
EOF

# 4. Fix Apache configuration
sudo tee /etc/apache2/sites-available/000-default.conf > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # Trust proxy headers
    RemoteIPHeader X-Forwarded-For
    RemoteIPInternalProxy 192.168.100.20
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# 5. Enable required modules
sudo a2enmod rewrite
sudo a2enmod remoteip

# 6. Clear WordPress cache directories
sudo rm -rf /var/www/html/wordpress/wp-content/cache/*
sudo rm -rf /var/www/html/wordpress/wp-content/uploads/wp-rocket/* 2>/dev/null

# 7. Restart Apache
sudo systemctl restart apache2

echo "✅ Fixes applied!"
