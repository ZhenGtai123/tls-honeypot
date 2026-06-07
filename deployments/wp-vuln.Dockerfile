FROM wordpress:5.9-php7.4-apache

# Install WP-CLI
RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    && chmod +x wp-cli.phar \
    && mv wp-cli.phar /usr/local/bin/wp

# Make sure WP files are writable
RUN chown -R www-data:www-data /var/www/html