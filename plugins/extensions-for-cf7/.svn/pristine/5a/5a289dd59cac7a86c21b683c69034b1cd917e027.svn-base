<?php
	$condition_mode = htcf7ext_get_option('htcf7ext_opt', 'conditional_mode', 'normal');
	$animation_enable = htcf7ext_get_option('htcf7ext_opt', 'animation_enable', 'on');
	$admimation_in_time = htcf7ext_get_option('htcf7ext_opt', 'admimation_in_time', '250');
	$admimation_out_time = htcf7ext_get_option('htcf7ext_opt', 'admimation_out_time', '250');
?>
<div id="extcf7-conditional-wraper">
	<table class="form-table" role="presentation">
		<tbody>
			<tr>
				<th scope="row"><?php echo esc_html__('Conditional Ui Mode','cf7-extensions');?></th>
				<td>
					<select name="conditional_mode">
						<option value="normal" <?php echo $condition_mode == 'normal' ? 'selected' : ''; ?>><?php echo esc_html__('Normal','cf7-extensions'); ?></option>
						<option value="text" <?php echo $condition_mode == 'text' ? 'selected' : ''; ?>><?php echo esc_html__('Text Mode','cf7-extensions'); ?></option>
					</select>
					<p><?php echo esc_html__('Set the Conditional Ui mode.(Default:Normal)','cf7-extensions') ?></p>
				</td>
			</tr>
			<tr class="extcf7-animation-status">
				<th scope="row"><?php echo esc_html__('Animation','cf7-extensions');?></th>
				<td class="extcf7-checkbox">
					<input type="hidden" name="animation_enable" value="off">
					<input type="checkbox" class="checkbox" id="extcf7-animation-enable" name="animation_enable" value="on" <?php echo $animation_enable == 'on' ? 'checked' : '';?>>
					<label for="extcf7-animation-enable"></label>
					<p><?php echo esc_html__('Enable Conditional Field Animation to show and hide field.','cf7-extensions');?></p>
				</td>
			</tr>
			<tr class="extcf7-animation-time">
				<th scope="row"><?php echo esc_html__('Animation In Time','cf7-extensions');?></th>
				<td>
					<input type="text" class="regular-text" name="admimation_in_time" value="<?php echo esc_attr($admimation_in_time); ?>">
					<p><?php echo esc_html__('Input a positive integer value for animation in time. The values in milliseconds and it will be applied for each field. Default Value:250','cf7-extensions'); ?></p>
				</td>
			</tr>
			<tr class="extcf7-animation-time">
				<th scope="row"><?php echo esc_html__('Animation Out Time','cf7-extensions');?></th>
				<td>
					<input type="text" class="regular-text" name="admimation_out_time" value="<?php echo esc_attr($admimation_out_time); ?>">
					<p><?php echo esc_html__('Input a positive integer value for animation out time. The values in milliseconds and it will be applied for each field. Default Value:250','cf7-extensions'); ?></p>
				</td>
			</tr>
		</tbody>
	</table>
	<div class="cf7-editor-link">
		<?php 
	        $link = admin_url().'admin.php?page=wpcf7';
		?>
		<a href="<?php echo esc_url($link); ?>"><?php echo esc_html__('Go To Contact Form 7 Editor','cf7-extensions'); ?></a>
	</div>
</div>