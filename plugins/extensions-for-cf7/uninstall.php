<?php
/*
 * HT CF7 EMAIL uninstall pluign
*/

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) exit; // Exit if accessed directly

include_once dirname( __FILE__ ) . '/includes/class.installer.php';

function extcf7_email_uninstall(){
	//Delete Table
	Extensions_Cf7_Installer::drop_tables();
}
extcf7_email_uninstall();