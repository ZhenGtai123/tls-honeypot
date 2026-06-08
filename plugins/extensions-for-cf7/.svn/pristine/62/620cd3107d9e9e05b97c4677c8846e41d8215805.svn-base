<h2>MailChimp</h2>
<div class="extcf7-mailchimp-pannel-wraper">
	<div class="extcf7__row">
		<div class="extcf7-feild-half">
			<div class="extcf7__box">
				<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-api-key"><strong><?php echo esc_html__('MailChimp Api Key:','cf7-extensions-pro') ?></strong></label>
				<input id="extcf7-mailchimp-api-key" class="wide" size="50" type="text" name="extcf7-mailchimp[api]" value="<?php echo isset($extcf7_mcmp['api']) ? esc_attr($extcf7_mcmp['api']) : ''?>">
				<span class="extcf7-mailchimp-activate-btn">
					<input id="extcf7-mailchimp-activate" type="button" class="button extcf7-md-btn" value="Connect With MailChimp">
					<span class="dashicons dashicons-no"></span>
					<span class="spinner"></span>
				</span>
				<input type="hidden" id="malichimp-formid" name="extcf7-mailchimp[malichimp_formid]" value="<?php echo $form->id(); ?>" style="width:0%;">
				<small class="extcf7-description need-api">
					<span class="invalid-api-message">Invalid Api Key</span>
					<p>Don't know how to get a Mailchimp API key? Get it from <a class="extcf7-mailchiml-api-link"  href="<?php echo esc_url('https://mailchimp.com/help/about-api-keys/'); ?>" target="_blank"><?php echo esc_html__('here','cf7-extensions-pro') ?></a></p>
				</small>
			</div>
		</div>
		<div class="extcf7-feild-half extcf7-for-mobile">
			<div class="extcf7-custom-fields extcf7-mailchimp-activated extcf7-mailchimp-inactive">
				<?php if(isset($extcf7_mcmp['valid_api'])): ?>
					<input type="hidden" id="ini-valid-api" name="extcf7-mailchimp[valid_api]" value="<?php echo esc_attr( $extcf7_mcmp['valid_api'] ) ; ?>" />
					<div id="extcf7-listmail">
						<?php echo $this->mailchimp_html_listmail($extcf7_mcmp['valid_api'],$extcf7_mcmp['lisdata']); ?>
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
							<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-emalil"><?php echo esc_html__( 'Subscriber Email', 'cf7-extensions-pro' ); ?></label>
							<?php $this->cf7_form_tag_html('email', $cf7_list_tag, $extcf7_mcmp, 'email', false); ?>
							<small class="extcf7-mailchimp-desc"><?php echo esc_html__( "This field will receive subscriber emails so, make sure to select the email tag.", "cf7-extensions-pro" ) ?> ( <span class="extcf7-required" >Required</span> )</small>
						</div>
					</div>
					<div class="extcf7-feild-half">
						<div class="extcf7_p_lr_tb">
							<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-emalil"><?php echo esc_html__( 'Subscriber Name ', 'cf7-extensions-pro' ); ?></label>
							<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $extcf7_mcmp, 'text', false); ?>
							<small class="extcf7-mailchimp-desc"><?php echo esc_html__( "Selected tag will be send as subscriber name.","cf7-extensions-pro" ) ?> ( <span class="extcf7-required" >Required</span> )</small>
						</div>
					</div>
				</div>
			</div>
			<div class="extcf7-custom-fields extcf7_p_lr_tb">
				<table class="form-table ">
					<tbody>
						<tr>
							<th scope="row">Custom Fields</th>
							<td>
								<label for="extcf7-mailchimp-custom-field">
									<input type="checkbox" id="extcf7-mailchimp-custom-field" name="extcf7-mailchimp[chimp-customfield]" value="1" <?php echo ( isset($extcf7_mcmp['chimp-customfield']) ) ? ' checked="checked"' : ''; ?>><?php echo esc_html( __( 'Add more fields to send Mailchimp.com', 'cf7-extensions-pro' ) ); ?>
								</label>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="extcf7-chimp-customfield">
					<p><strong><?php echo esc_html__( 'Map Contact Form 7 Fields with Mailchimp Field', 'cf7-extensions-pro' ); ?></strong></p>
					<?php if(isset($extcf7_mcmp['cf7tag']) && (isset($extcf7_mcmp['mailchimp-tag']) && !empty($extcf7_mcmp['mailchimp-tag']))): 
						$cf7_tag = $extcf7_mcmp['cf7tag']; 
						for ($i=0; $i < count($cf7_tag); $i++) { 
							?>
								<div class="extcf7-mailchimp-custom-fields" data-mcmp_csmfield='yes'>
									<div class="col-3">
										<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Contact Form Field','cf7-extensions-pro') ?></strong></label>
											<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $cf7_tag[$i], 'text', true); ?>
									</div>
									<div class="col-3" id="extcf7-mailchimp-field">
										<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Mailchimp Field','cf7-extensions-pro') ?></strong></label>
						                <select name="extcf7-mailchimp[mailchimp-tag][]" style="width:95%;">
						                    <?php foreach ( $extcf7_mcmp['listfields'] as $field ): ?>
						                        <option value="<?php echo $field['name'] ?>" <?php  if ( $extcf7_mcmp['mailchimp-tag'][$i] == $field['name'] ) { echo 'selected="selected"'; } ?>><?php echo $field['label']; ?></option>
						                    <?php endforeach; ?>
						                </select>
					            	</div>
					            	<button id="extcf7-custom-field-delete" class="button">remove</button>
					            </div>
							<?php	
						}
					?>

					<?php else: ?>
						<div class="extcf7-mailchimp-custom-fields" data-mcmp_csmfield='no'>
							<div class="col-3">
								<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Contact Form Field','cf7-extensions-pro') ?></strong></label>
									<?php $this->cf7_form_tag_html('name', $cf7_list_tag, $extcf7_mcmp, 'text', true); ?>
							</div>
							<?php if(!isset($extcf7_mcmp['listfields']) || empty($extcf7_mcmp['listfields'])): ?>
								<div class="col-3" id="extcf7-mailchimp-field">
								</div>
							<?php else: ?>
								<div class="col-3" id="extcf7-mailchimp-field">
									<label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Mailchimp Field','cf7-extensions-pro') ?></strong></label>
					                <select name="extcf7-mailchimp[mailchimp-tag][]" style="width:95%;">
					                    <?php foreach ( $extcf7_mcmp['listfields'] as $field ): ?>
					                        <option value="<?php echo $field['name'] ?>"><?php echo $field['label']; ?></option>
					                    <?php endforeach; ?>
					                </select>
				            	</div>
				            <?php endif; ?>
			        	</div>
					<?php endif; ?>		
					<div class="extcf7-custom-button-align">
						<button id="extcf7-add-custom-field" class="button extcf7-md-btn ">Add Custom Field</button>
					</div>
				</div>
			</div>
			<div class="extcf7-custom-fields extcf7_p_lr_tb">
				<table class="form-table">
					<tbody>
						<tr>
							<th scope="row">Subscription</th>
							<td>
								<label for="extcf7-mailchimp-enable">
									<input type="checkbox" id="extcf7-mailchimp-enable" name="extcf7-mailchimp[chimp-active]" value="1" <?php echo ( isset($extcf7_mcmp['chimp-active']) ) ? ' checked="checked"' : ''; ?>><?php echo esc_html( __( 'Disable', 'cf7-extensions-pro' ) ); ?>
								</label>
							</td>
						</tr>
						<tr>
							<th>Required User Aacceptance</th>
							<td>
								<input type="text" name="extcf7-mailchimp[confirm-subs]" class="regular-text" value="<?php echo (isset($extcf7_mcmp['confirm-subs'])) ? $extcf7_mcmp['confirm-subs'] : '';?>">
								<div class="extcf7-tooptip-wraper">
									<p>- To create forms with user acceptability like </p>
									<div class="extcf7-tooltip-item">
										<a href="#">&#8505;</a>
										<div class="tooltip">
										  <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL.'admin/assets/images/acceptence-1.png');?>" alt=""/>
										</div>
									</div>
								</div>
								<div class="extcf7-tooptip-wraper">
									<p>- Configure your form in exactly the same way as the </p>
									<div class="extcf7-tooltip-item">
										<a href="#">&#8505;</a>
										<div class="tooltip">
										  <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL.'admin/assets/images/acceptence-2.png');?>" alt=""/>
										</div>
									</div>
								</div>
								<div class="extcf7-tooptip-wraper">
									<p>- Use the tag [confirm-subscribe] in the MailChimp's settings as like </p>
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
	var init_valid_api = <?php echo isset($extcf7_mcmp['valid_api']) ? $extcf7_mcmp['valid_api'] : 0; ?>;
	var custom_field_visible = <?php echo isset($extcf7_mcmp['chimp-customfield']) ? $extcf7_mcmp['chimp-customfield'] : '0'; ?>;
</script>