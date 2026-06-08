<?php
/**
 * Plugin Name: Extensions For CF7 
 * Description: Valuable Extensions for Contact Form 7.
 * Author: 		HasThemes
 * Author URI: 	https://hasthemes.com/
 * Version: 	3.1.9
 * Text Domain: cf7-extensions
 * Domain Path: /languages
*/

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly
define( 'CF7_EXTENTIONS_PL_ROOT', __FILE__ );
define( 'CF7_EXTENTIONS_PL_URL', plugins_url( '/', CF7_EXTENTIONS_PL_ROOT ) );
define( 'CF7_EXTENTIONS_PL_PATH', plugin_dir_path( CF7_EXTENTIONS_PL_ROOT ) );
define( 'CF7_EXTENTIONS_PL_BASE', plugin_basename( CF7_EXTENTIONS_PL_ROOT ) );
define( 'CF7_EXTENTIONS_PL_VERSION', '3.1.9' );

/**
 * CF7 Form Data list render interface
*/
interface Extensions_Cf7_Form_Datalist_Render{
	function cf7_layout_render();
}

//Required File
require_once ( CF7_EXTENTIONS_PL_PATH .'includes/class.installer.php');
require_once ( CF7_EXTENTIONS_PL_PATH .'includes/class.cf7-extensions.php');