<?php 
	$ip_address_enable = htcf7ext_get_option('htcf7ext_opt', 'ip_address_enable', 'on');
	$reffer_link_enable = htcf7ext_get_option('htcf7ext_opt', 'reffer_link_enable', 'on');
?>

<div id="extcf7_pro-general-settings-wraper">
	<table class="form-table" role="presentation">
		<tbody>
			<tr>
				<th scope="row"><?php echo esc_html__('IP Address','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="ip_address_enable" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-ip-address-enable" name="ip_address_enable" value="on" <?php echo $ip_address_enable == 'on' ? 'checked' : '';?>>
					<label for="extcf7-ip-address-enable"></label>
					<p><?php echo esc_html__('Enable this option to make the sender\'s IP Address visible.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr>
				<th scope="row"><?php echo esc_html__('Referer Link','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="reffer_link_enable" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-referer-link-enable" name="reffer_link_enable" value="on" <?php echo $reffer_link_enable == 'on' ? 'checked' : '';?>>
					<label for="extcf7-referer-link-enable"></label>
					<p><?php echo esc_html__('Enable this option to make the referrer link visible.','cf7-extensions');?></p>
				</td>
			</tr>
		</tbody>
	</table>
</div>