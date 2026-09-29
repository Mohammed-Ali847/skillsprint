# ApexNova Enterprise Information Security Policy
Doc Code: DOC-POL-01 | Type: POLICY | Version: 2.0
Department: CYBER_SEC | Organization: ApexNova Global Technologies

## Section 1.1: Purpose & Organizational Scope
This policy establishes corporate information security controls across ApexNova Global Technologies, governing all cloud assets, infrastructure, and employee equipment.

## Section 1.2: Identity Authentication & MFA Standard
All corporate accounts must enforce passphrases of at least 16 characters with symbols, uppercase, lowercase, and digits. Passphrases must be rotated every 90 days. SMS MFA is strictly deprecated; FIDO2 hardware keys or authenticator apps are mandatory for all production and customer-facing staff.

## Section 1.3: Workstation Auto-Lock & Clean Desk Standard
Unattended workstations must automatically lock screen after 5 minutes of inactivity. Workstations must maintain a clean desk posture free of written credentials or customer identifiers.

## Section 1.4: Data Encryption Standards
All data at rest must use AES-256 encryption. All data in transit must enforce TLS 1.3 encryption. Unencrypted storage of client records on local hard drives is strictly prohibited.

## Section 1.5: Removable Storage Media Ban
Use of unencrypted USB flash drives, personal external storage devices, or unauthorized mass media is strictly prohibited on corporate laptops.

