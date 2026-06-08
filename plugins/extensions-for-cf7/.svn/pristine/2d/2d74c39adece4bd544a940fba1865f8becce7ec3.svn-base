<?php
/**
 * Installer class
 * @phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared, WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching, WordPress.DB.DirectDatabaseQuery.SchemaChange
 */
class Extensions_Cf7_Installer {

    /**
     * Run the installer
     *
     * @return void
    */
    public function run() {
        $this->create_tables();
    }

    /**
     * [create_tables]
     * @return [void]
    */
    public function create_tables() {
        global $wpdb;

        $table_name = $wpdb->prefix .'extcf7_db';

        $charset_collate = $wpdb->get_charset_collate();

        $schema = "
        CREATE TABLE IF NOT EXISTS $table_name (
        id bigint(9) NOT NULL AUTO_INCREMENT,
        form_id bigint(55) DEFAULT NULL,
        form_value longtext NOT NULL,
        form_date datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
        PRIMARY KEY  (id)
        ) $charset_collate;
        ";

        if ( ! function_exists( 'dbDelta' ) ) {
            require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        }

        dbDelta( $schema );
        delete_option('extcf7_db_table_alter_status');
    }

    /**
     * [drop_tables] Delete table
     * @return [void]
    */
    public static function drop_tables() {
        global $wpdb;
        $tables = [
            "{$wpdb->prefix}extcf7_db",
        ];
        foreach ( $tables as $table ) {
            $wpdb->query( "DROP TABLE IF EXISTS {$table}" );
        }
    }
}