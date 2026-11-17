from classifier import process_ticket

# 20 diverse test tickets across all 6 categories and severities
test_suite = [
    # Network
    ("WiFi is not working in conference room 2B", "Network", "Medium"),
    ("Internet connection is very slow across floor 3", "Network", "Medium"),
    ("Office LAN cable disconnected no network access", "Network", "Medium"),
    ("Entire company network is down business stopped", "Network", "Critical"),
    
    # VPN
    ("VPN is not connecting and I have a client meeting in 30 minutes", "VPN", "High"),
    ("Unable to access company VPN from remote location", "VPN", "High"),
    ("Cisco AnyConnect VPN error failed to authenticate", "VPN", "High"),
    ("URGENT: VPN connection timeout cannot access client portal", "VPN", "High"),
    
    # Password
    ("I forgot my password please reset", "Password", "Low"),
    ("Account is locked after too many attempts need password reset", "Password", "Low"),
    ("Two-factor authentication 2FA token expired cannot login", "Password", "Medium"),
    ("Please unlock password for corporate email", "Password", "Low"),
    
    # Software
    ("Install Microsoft Office 365 on my laptop", "Software", "Low"),
    ("Application installation required for Docker Desktop", "Software", "Low"),
    ("Need Zoom meetings application installed for team calls", "Software", "Low"),
    ("VS Code extension crashing after software update", "Software", "Medium"),
    
    # Hardware
    ("Laptop keyboard is not working keys broken unresponsive", "Hardware", "Medium"),
    ("Monitor display is not working blank black screen", "Hardware", "Medium"),
    ("Printer not responding paper jam issue on floor 2", "Hardware", "Medium"),
    
    # System
    ("Entire production server is down critical outage", "System", "Critical")
]

cat_correct = 0
sev_correct = 0
total = len(test_suite)

print("Running Milestone 1 Evaluation Test Suite...\n" + "=" * 55)

for text, expected_cat, expected_sev in test_suite:
    pred_cat, pred_sev, pred_pri, conf = process_ticket(text)
    if pred_cat == expected_cat:
        cat_correct += 1
    if pred_sev == expected_sev:
        sev_correct += 1

cat_acc = (cat_correct / total) * 100
sev_acc = (sev_correct / total) * 100

print(f"Classification Accuracy : {cat_correct}/{total} = {cat_acc:.1f}%  (Target: ≥ 90% | {'PASS' if cat_acc >= 90 else 'CHECK'})")
print(f"Severity Accuracy       : {sev_correct}/{total} = {sev_acc:.1f}%  (Target: ≥ 85% | {'PASS' if sev_acc >= 85 else 'CHECK'})")
print("=" * 55)