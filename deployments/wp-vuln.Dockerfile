FROM wordpress:5.9-php7.4-apache

# Copy plugin
COPY ./honeypot/wordpress-https-vurn/all-in-one-wp-migration/ /var/www/html/wp-content/plugins/all-in-one-wp-migration/

# Ensure writable permissions
RUN chown -R www-data:www-data /var/www/html/wp-content/plugins