<div class="extcf7-inner-container">
	<label class="extcf7-switch" id="extcf7-text-only-switch">
		<span class="extcf7-toggle-label"><?php echo esc_html__( 'Go To Text mode', 'cf7-extensions' ); ?></span>
		<span class="extcf7-toggle-mode">
			<input type="checkbox" id="extcf7-text-only-checkbox" name="extcf7-text-only-checkbox" value="text_only">
			<span class="mode-slider round"></span>
		</span>
	</label>
	<h2><?php echo esc_html__( 'Conditional fields', 'cf7-extensions' ); ?></h2>
	<div id="extcf7-entries-ui">
		<div id="extcf7-new-entry">
			<div class="extcf7-if">
                <span class="extcf7-show-label"><?php echo esc_html__( 'Show', 'cf7-extensions' ); ?></span>
                <select class="extcf7-then-field">
                	<?php echo $this->extcf7_all_group_options($form); //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
                </select>
            </div>
			<div class="extcf7-and-rules-container">
				<div class="extcf7-and-rule">
                    <span class="extcf7-if-txt-label"></span>
                    <select class="extcf7-if-field-select">
                    	<?php echo $this->extcf7_all_field_options($form); //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
                    </select>
                    <select class="extcf7-condition-operator_input">
                    	<option value="equal"><?php echo esc_html__('equal','cf7-extensions'); ?></option>
                    	<option value="not-equal"><?php echo esc_html__('not equal','cf7-extensions'); ?></option>
                    </select>
                    <input class="extcf7-if-field-value" type="text" placeholder="<?php echo esc_attr( 'value'); ?>" value="">
                    <span  class="extcf7-delete-button">&#10005;</span>
                </div>
                <span class="extcf7-and-button"><?php echo esc_html__( 'Add Condition', 'cf7-extensions' ); ?></span>
			</div>
			<span class="extcf7-remove-condition-btn">x</span>
		</div>
		<div id="extcf7-entries">

		</div>
		<span id="extcf7-add-button" title="<?php echo esc_attr('add new condition rule'); ?>"><?php echo esc_html__( 'Add New Condition', 'cf7-extensions'); ?></span>
		<div class="extcf7-user-notice">
			<p><?php esc_html_e('If You use a single input checkbox field for condition, then You have to fill the conditional value filed with "checked".','cf7-extensions');?></p>
		</div>
	</div>
	<div id="extcf7-text-entries">
        <div id="extcf7-settings-text-wrap">
            <textarea id="extcf7-settings-text" name="extcf7-settings-text"><?php 
            echo Extensions_Cf7_Condition_Setup::serialize_conditions_value($extcf7_entries);  //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
            ?></textarea>
            <br>
        </div>
    </div>
    <div class="extcf7-conditional-settings-link">
		<?php
		   	$link = admin_url().'admin.php?page=cf7-conditional-settings';
		?>
		<a href="<?php echo esc_url($link); ?>"><?php echo esc_html__('Go To Conditional Settings','cf7-extensions') ?></a>
	</div>
</div>