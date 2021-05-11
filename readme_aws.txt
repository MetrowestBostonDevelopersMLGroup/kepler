Here are steps to set up AWS EC2 including X-desktop access via TightVNC with stumbling blocks to avoid.

Create an AWS account and stand up the EC2 Server:
https://aws.amazon.com/   Create an account.
https://aws.amazon.com/  ->  My Account -> Root User -> (login)
Services (dropdown) -> EC2 -> 
Launch Instances ->  Choose a free tier - I used Ubuntu 20  64bit x86 -> T2 micro (free tier eligible)
"Configure Instance Details"  -> disk space (second page of options) increase to 30GB
Take rest of defaults
Create a keypair with a project.specific name and download.  AWS will require privs on this file set to disallow group and world.  Assuming you have a linux shell on your desktop, such as the handy and excellent Windows Subsystem for Linux  https://docs.microsoft.com/en-us/windows/wsl/install-win10   the steps are:
cd ~
cp /mnt/c/Users/Youraccount/Downloads/yourpenfile.pem ~/
chmod 700 yourpemfile.pem.
Your EC2 will spin up - visit the AWS Console, find the new instance
Give the instance a name - my example assumes "metrowest_kepler"

Accessing your EC2:
You can access via ssh (command line) or TightVNC to the X desktop.  To set up the latter you need the former.

Terminal/SSH access:
From AWS console highlight the instance -> Connect -> SSH  and copy/paste the command.  It will be something like:
ssh -i "metrowest_kepler.pem" ubuntu@ec2-12-34-56-789.us-east-2.compute.amazonaws.com
you will be logged as user "ubuntu"

TightVNC to X-desktop
Follow the excellent reference https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-ubuntu-18-04

---NOTE three stumbling blocks ---

You need to open port 5901 on the server.  Go to AWS console -> Instance -> Security -> Security Group -> edit inbound rules -> Add Rule -> 5901  and 0.0.0.0/0 -> Save Rules.  Repeat for outbound rule for that security group.  The rule takes effect immediately (no need to re-start).

When port-forwarding 5901, the instructions say
ssh -L 5901:127.0.0.1:5901 -C -N -l sammy your_server_ip
This did not work because I am using .pem file.  Instead:
ssh -L 5901:127.0.0.1:5901 -C -N -i  "metrowest_kepler.pem" ubuntu@ec2-00-123-4-567.us-east-2.compute.amazonaws.com

When using TightVNC on your desktop use the Public IPv4 address and note the double-colons (that is not a typo) e.g. 12.345.6.789::5901



