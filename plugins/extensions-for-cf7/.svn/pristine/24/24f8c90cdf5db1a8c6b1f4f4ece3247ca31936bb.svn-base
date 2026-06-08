<h2><?php echo esc_html__('MailChimp', 'cf7-extensions'); ?></h2>
<div class="extcf7-mailchimp-pannel-wraper">
	<div class="extcf7__row">
		<div class="extcf7-feild-half">
		<?php
		if( ! empty( $extcf7_mcmp['api'] ) ) {
			$length = strlen( $extcf7_mcmp['api'] );
			$replace_length = 20;
			$start_position = floor(($length - $replace_length) / 2);
			$replacement = str_repeat('#', $replace_length);
			$api_generated_string = substr_replace($extcf7_mcmp['api'], $replacement, $start_position, $replace_length);
		}
		?>
			<div class="extcf7__box">
				<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-api-key"><strong><?php echo esc_html__('MailChimp Api Key:','cf7-extensions') ?></strong></label>
				<input id="extcf7-mailchimp-api-key" class="wide" size="50" type="text" name="extcf7-mailchimp[api]" value="<?php echo isset( $api_generated_string ) ? esc_attr( $api_generated_string ) : ''; ?>">
				<span class="extcf7-mailchimp-activate-btn">
					<input id="extcf7-mailchimp-activate" type="button" class="button extcf7-md-btn" value="<?php esc_attr_e('Connect With MailChimp','cf7-extensions');?>">
					<span class="dashicons dashicons-no"></span>
					<span class="spinner"></span>
				</span>
				<input type="hidden" id="malichimp-formid" name="extcf7-mailchimp[malichimp_formid]" value="<?php echo esc_attr($form->id()); ?>" style="width:0%;">
				<small class="extcf7-description need-api">
					<span class="invalid-api-message"><?php esc_html_e('Invalid Api Key','cf7-extensions');?></span>
					<p><?php esc_html_e('Don\'t know how to get a Mailchimp API key? Get it from', 'cf7-extensions');?> <a class="extcf7-mailchiml-api-link"  href="<?php echo esc_url('https://mailchimp.com/help/about-api-keys/'); ?>" target="_blank"><?php echo esc_html__('here','cf7-extensions') ?></a></p>
				</small>
			</div>
		</div>
		<div class="extcf7-feild-half extcf7-for-mobile">
			<div class="extcf7-custom-fields extcf7-mailchimp-activated extcf7-mailchimp-inactive">
				<?php if(isset($extcf7_mcmp['valid_api'])): ?>
					<input type="hidden" id="ini-valid-api" name="extcf7-mailchimp[valid_api]" value="<?php echo esc_attr( $extcf7_mcmp['valid_api'] ) ; ?>" />
					<div id="extcf7-listmail">
						<?php echo $this->mailchimp_html_listmail($extcf7_mcmp['valid_api'],$extcf7_mcmp['lisdata']); //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
					</div>
				<?php else: ?>
					<div id="extcf7-listmail"></div>
				<?php endif; ?>
			</div>
		</div>
	</div>
	


	
	<div class="extcf7-mailchimp-activated extcf7-mailchimp-inactive">
		<div class="extcf7-activated-wraper">
			<div class="extcf7-custom-fields extcf7_p_lr_tb">
				<div class="extcf7__row ">
					<div class="extcf7-feild-half">
						<div class="extcf7_p_lr_tb">
							<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-emalil"><?php echo esc_html__( 'Subscriber Email', 'cf7-extensions' ); ?></label>
							<?php $this->cf7_form_tag_html('email', $cf7_list_tag, $extcf7_mcmp, 'email', false); ?>
							<small class="extcf7-mailchimp-desc"><?php echo esc_html__( "This field will receive subscriber emails so, make sure to select the email tag.", "cf7-extensions" ) ?> ( <span class="extcf7-required" ><?php esc_html_e('Required','cf7-extensions');?></span> )</small>
						</div>
					</div>
					<div class="extcf7-feild-half">
						<div class="extcf7_p_lr_tb">
							<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-emalil"><?php echo esc_html__( 'Subscriber Name ', 'cf7-extensions' ); ?></label>
							<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $extcf7_mcmp, 'text', false); ?>
							<small class="extcf7-mailchimp-desc"><?php echo esc_html__( "Selected tag will be send as subscriber name.","cf7-extensions" ) ?> ( <span class="extcf7-required" ><?php esc_html_e('Required','cf7-extensions');?></span> )</small>
						</div>
					</div>
				</div>
			</div>
			<div class="extcf7-custom-fields extcf7_p_lr_tb">
				<table class="form-table ">
					<tbody>
						<tr>
							<th scope="row"><?php __('Custom Fields', 'cf7-extensions') ?></th>
							<td>
								<label for="extcf7-mailchimp-custom-field">
									<input type="checkbox" id="extcf7-mailchimp-custom-field" name="extcf7-mailchimp[chimp-customfield]" value="1" <?php echo ( isset($extcf7_mcmp['chimp-customfield']) ) ? ' checked="checked"' : ''; ?>><?php echo esc_html( __( 'Add more fields to send Mailchimp.com', 'cf7-extensions' ) ); ?>
								</label>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="extcf7-chimp-customfield">
					<p><strong><?php echo esc_html__( 'Map Contact Form 7 Fields with Mailchimp Field', 'cf7-extensions' ); ?></strong></p>
					<?php if(isset($extcf7_mcmp['cf7tag']) && (isset($extcf7_mcmp['mailchimp-tag']) && !empty($extcf7_mcmp['mailchimp-tag']))): 
						$cf7_tag = $extcf7_mcmp['cf7tag']; 
						for ($i=0; $i < count($cf7_tag); $i++) { 
							?>
								<div class="extcf7-mailchimp-custom-fields" data-mcmp_csmfield='yes'>
									<div class="col-3">
										<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Contact Form Field','cf7-extensions') ?></strong></label>
											<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $cf7_tag[$i], 'text', true); ?>
									</div>
									<div class="col-3" id="extcf7-mailchimp-field">
										<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Mailchimp Field','cf7-extensions') ?></strong></label>
						                <select name="extcf7-mailchimp[mailchimp-tag][]" style="width:95%;">
						                    <?php foreach ( $extcf7_mcmp['listfields'] as $field ): ?>
						                        <option value="<?php echo esc_attr($field['name']) ?>" <?php  if ( $extcf7_mcmp['mailchimp-tag'][$i] == $field['name'] ) { echo 'selected="selected"'; } ?>><?php echo esc_html($field['label']); ?></option>
						                    <?php endforeach; ?>
						                </select>
					            	</div>
					            	<button id="extcf7-custom-field-delete" class="button"><?php esc_html_e('Remove','cf7-extensions');?></button>
					            </div>
							<?php	
						}
					?>

					<?php else: ?>
						<div class="extcf7-mailchimp-custom-fields" data-mcmp_csmfield='no'>
							<div class="col-3">
								<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Contact Form Field','cf7-extensions') ?></strong></label>
									<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $extcf7_mcmp, 'text', true); ?>
							</div>
							<?php if(!isset($extcf7_mcmp['listfields']) || empty($extcf7_mcmp['listfields'])): ?>
								<div class="col-3" id="extcf7-mailchimp-field">
								</div>
							<?php else: ?>
								<div class="col-3" id="extcf7-mailchimp-field">
									<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Mailchimp Field','cf7-extensions') ?></strong></label>
					                <select name="extcf7-mailchimp[mailchimp-tag][]" style="width:95%;">
					                    <?php foreach ( $extcf7_mcmp['listfields'] as $field ): ?>
					                        <option value="<?php echo esc_attr($field['name']) ?>"><?php echo esc_html($field['label']); ?></option>
					                    <?php endforeach; ?>
					                </select>
				            	</div>
				            <?php endif; ?>
			        	</div>
					<?php endif; ?>		
					<div class="extcf7-custom-button-align">
						<button id="extcf7-add-custom-field" class="button extcf7-md-btn "><?php esc_html_e('Add Custom Field','cf7-extensions');?></button>
					</div>
				</div>
			</div>
			<div class="extcf7-custom-fields extcf7_p_lr_tb">
				<table class="form-table">
					<tbody>
						<tr>
							<th scope="row"><?php esc_html_e('Subscription','cf7-extensions');?></th>
							<td>
								<label for="extcf7-mailchimp-enable">
									<input type="checkbox" id="extcf7-mailchimp-enable" name="extcf7-mailchimp[chimp-active]" value="1" <?php echo ( isset($extcf7_mcmp['chimp-active']) ) ? ' checked="checked"' : ''; ?>><?php echo esc_html__( 'Disable', 'cf7-extensions' ); ?>
								</label>
							</td>
						</tr>
						<tr>
							<th><?php esc_html_e('Required User Aacceptance','cf7-extensions');?></th>
							<td>
								<input type="text" name="extcf7-mailchimp[confirm-subs]" class="regular-text" value="<?php echo (isset($extcf7_mcmp['confirm-subs'])) ? esc_attr($extcf7_mcmp['confirm-subs']) : '';?>">
								<div class="extcf7-tooptip-wraper">
									<p><?php esc_html_e('- To create forms with user acceptability like','cf7-extensions');?> </p>
									<div class="extcf7-tooltip-item">
										<a href="#">&#8505;</a>
										<div class="tooltip">
										  <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL.'admin/assets/images/acceptence-1.png');?>" alt=""/>
										</div>
									</div>
								</div>
								<div class="extcf7-tooptip-wraper">
									<p><?php esc_html_e('- Configure your form in exactly the same way as the','cf7-extensions');?> </p>
									<div class="extcf7-tooltip-item">
										<a href="#">&#8505;</a>
										<div class="tooltip">
										  <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL.'admin/assets/images/acceptence-2.png');?>" alt=""/>
										</div>
									</div>
								</div>
								<div class="extcf7-tooptip-wraper">
									<p><?php esc_html_e('- Use the tag [confirm-subscribe] in the MailChimp\'s settings as like','cf7-extensions');?> </p>
									<div class="extcf7-tooltip-item">
										<a href="#">&#8505;</a>
										<div class="tooltip">
										  <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL.'admin/assets/images/acceptence-3.png');?>" alt=""/>
										</div>
									</div>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
<script type="text/javascript">
	var init_valid_api = <?php echo isset($extcf7_mcmp['valid_api']) ? esc_js($extcf7_mcmp['valid_api']) : 0; ?>;
	var custom_field_visible = <?php echo isset($extcf7_mcmp['chimp-customfield']) ? esc_js($extcf7_mcmp['chimp-customfield']) : '0'; ?>;
</script>