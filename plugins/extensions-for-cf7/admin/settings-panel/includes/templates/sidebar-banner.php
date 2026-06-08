<?php 
ob_start(); 
?>
<div class="htoptions-sidebar-adds-area">
    <div class="htcf7ext-opt-get-pro">
        <h3 class="htcf7ext-opt-get-pro-title">Upgrade to Pro</h3>
        <ul>
            <li>Repeater Field</li>
            <li>Drag & Drop File Upload</li>
            <li>Advanced Telephone (Flag and Country Code)</li>
            <li>GDPR Field to take permission</li>
            <li>Already Submitted Message</li>
            <li>Validation Message in Popup</li>
        </ul>
        <a href="https://hasthemes.com/plugins/cf7-extensions?utm_source=cf7-free-plugin&utm_medium=cf7-plugin-admin&utm_campaign=cf7-admin-sidebar" class="button htcf7ext-opt-get-pro-btn" target="_blank">Get Pro Now</a>
    </div>

    <div class="htcf7ext-opt-support">
        <img src="<?php echo esc_url(CF7_EXTENTIONS_PL_URL) ?>/admin/settings-panel/assets/images/icons/customer-service.png" alt="Support And Feedback" width="65" height="65">
        <h3 class="htcf7ext-opt-support-title">Support And Feedback</h3>
        <p>If you have any questions, concerns, or feedback, please do not hesitate to reach out to us. We are always available and ready to assist you with your needs. Thank you for choosing our products and services, and we look forward to hearing from you soon!</p>
        <a href="https://hasthemes.com/contact-us/" class="button htcf7ext-opt-support-btn" target="_blank">Get Support</a>
    </div>
</div>
<?php echo apply_filters('htcf7ext_sidebar_adds_banner', ob_get_clean() ); ?>