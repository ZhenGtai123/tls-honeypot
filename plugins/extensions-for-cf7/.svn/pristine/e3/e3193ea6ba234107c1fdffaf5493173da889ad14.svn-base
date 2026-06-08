<?php 
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended
 */
	$pages = get_posts( array('post_type' => 'page', 'posts_per_page' => -1 ) );
	$redirect_options = get_post_meta($form_id,'extcf7_redirect_options',true);
	$redirection_enable = $redirect_options && is_array($redirect_options) ? $redirect_options['redirection_enable'] : 'off';
	$custom_url_enable = $redirect_options && is_array($redirect_options) ? $redirect_options['custom_url_enable'] : 'off';
	$redirect_page = $redirect_options && is_array($redirect_options) ? $redirect_options['redirect_page'] : "";
	$custom_urle = $redirect_options && is_array($redirect_options) ? $redirect_options['custom_urle'] : "";
	$js_action = $redirect_options && is_array($redirect_options) ? $redirect_options['js_action'] : 'off';
	$javascript_code = $redirect_options && is_array($redirect_options) ? $redirect_options['javascript_code'] : "";
	$redirect_new_tab = $redirect_options && is_array($redirect_options) ? $redirect_options['redirect_new_tab'] : "";
?>
<div class="extcf7-redirection-container">
	<h2><?php echo esc_html__('Redirection Options','cf7-extensions'); ?></h2>
	<table class="form-table" role="presentation">
		<tbody>
			<tr>
				<th scope="row"><?php echo esc_html__('Redirection','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="redirect_options[redirection_enable]" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-redirection-enable" name="redirect_options[redirection_enable]" value="on" <?php echo $redirection_enable == 'on' ? 'checked' : '';?>>
					<label for="extcf7-redirection-enable"></label>
					<p><?php echo esc_html__('Enable Redirection Option to redirect to any page after form submission.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr class="extcf7-redirect-fields">
				<th scope="row"><?php echo esc_html__('Custom URL','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="redirect_options[custom_url_enable]" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-custom-url-enable" name="redirect_options[custom_url_enable]" value="on" <?php echo $custom_url_enable == 'on' ? 'checked' : '';?>>
					<label for="extcf7-custom-url-enable"></label>
					<p><?php echo esc_html__('Enable Custom URL for Redirection.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr class="extcf7-page-url extcf7-redirect-fields">
				<th scope="row"><?php echo esc_html__('Select a page','cf7-extensions');?></th>
				<td>
					<select name="redirect_options[redirect_page]" class="regular-text">
					<option value="" selected><?php echo esc_html__('---select---','cf7-extensions');?></option>
					<?php foreach ($pages as $page):
					?>

						<option value="<?php echo esc_url(get_page_link($page->ID)); ?>" <?php echo $redirect_page == esc_url(get_page_link($page->ID))?'selected':''; ?>><?php echo esc_html($page->post_title) ?></option>

					<?php endforeach; ?>
					</select>
				</td>
			</tr>
			<tr class="extcf7-custom-page-url extcf7-redirect-fields">
				<th scope="row"><?php echo esc_html__('Custom URL','cf7-extensions');?></th>
				<td>
					<input type="text" class="regular-text" name="redirect_options[custom_urle]" value="<?php echo esc_attr($custom_urle); ?>">
					<p style="width: 750px;"><?php echo esc_html__('Insert a custom URL, if you want to add form field values as parameters in the custom redirection URL that you will insert here, just by adding the form field shortcodes to the URL. e.g. "https://example.com/?name=[you-name]"','cf7-extensions'); ?></p>
				</td>
			</tr>
			<tr class="extcf7-redirect-fields">
				<th scope="row"><?php echo esc_html__('Redirect to New Tab','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="redirect_options[redirect_new_tab]" value="off">
					<input type="checkbox" class="checkbox" id="redirect-new-tab" name="redirect_options[redirect_new_tab]" value="on" <?php echo $redirect_new_tab == 'on' ? 'checked' : '';?>>
					<label for="redirect-new-tab"></label>
					<p><?php echo esc_html__('Enable the option to open the redirection page in a new tab.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr>
				<th scope="row"><?php echo esc_html__('Javascript Action','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="redirect_options[js_action]" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-js-acction" name="redirect_options[js_action]" value="on" <?php echo $js_action == 'on' ? 'checked' : '';?>>
					<label for="extcf7-js-acction"></label>
					<p><?php echo esc_html__('Enable Javascript action to fire a javascript function.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr class="extcf7-js-code">
				<th scope="row"><?php echo esc_html__('Javascript Code','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<p ><?php echo esc_html__("Don't need to use <script> tag.",'cf7-extensions');?></p>
					<textarea rows="10" name="redirect_options[javascript_code]" class="regular-text" placeholder="Paste Your Javascript Code Here"><?php echo esc_html($javascript_code); ?></textarea>
					<p style="color: #a94442; background: #f2dede;padding: 15px;"><strong><?php echo esc_html__('Warnings!', 'cf7-extensions')?></strong><?php echo esc_html__("This options for developer only.If the javascript action doesn't work after form submission, it means You have a problem with your code.",'cf7-extensions');?></p>
				</td>
			</tr>
		</tbody>
	</table>
	<div class="cf7-editor-link">
		<?php
		   if(isset($_GET['post'])){
		   	 if(isset($_GET['active-tab'])){
		   	 	$link = admin_url().'admin.php?page=cf7-redirection-settings&from_id='.absint($_GET['post']).'&active_tab='.absint($_GET['active-tab']);
		   	 }else{
		   	 	$link = admin_url().'admin.php?page=cf7-redirection-settings&from_id='.absint($_GET['post']);
		   	 }
		   }else{
		   	 $link = admin_url().'admin.php?page=cf7-redirection-settings';
		   }
		?>
		<a href="<?php echo esc_url($link); ?>"><?php echo esc_html__('Go To Redirection Setting','cf7-extensions'); ?></a>
	</div>
	<script type="text/javascript">
		var extcf7_redirect_settings = <?php echo isset($redirect_options) && !empty($redirect_options) ? wp_json_encode($redirect_options) : '""'; ?>;
	</script>
</div>