---
authors:
    - Johan Hektor
date: 2020-05-05
---
# Setting up accounts for access to LUNARC resources
## SNIC account
Access to LUNARC resources, e.g. the Aurora cluster, is administered by [SNIC](https://snic.se).
1. The first step is therefore to set up a SNIC account in SUPR [here](https://supr.snic.se/person/register/).
If you are affiliated with a Swedish university you can most likely use the 'Register via SWAMID' option
2. You must then log in to SNIC and accept the user agreement; it is found under **Personal Information -> SNIC User Agreement**.
3. (Optional) You can also enable two-factor authentication for your account under **Personal Information -> Two-Factor Authentication (TOTP)**. This will require you to input a one time password generated by your cell phone each time you log in.

### Joining or applying for a project
To get access to the cluster you must belong to at least one SNIC project. You can apply for a new project or request to join an existing project in the SUPR portal.
#### Applying for a new project
##### Computing projects
You can apply for SNIC Compute projects [here](https://supr.snic.se/round/compute/?).
The projects come in different sizes depending on how much computing time (core-hours/month) you need.
A SNIC Small Compute project is likely enough in most cases.
These can be applied for by all scientists in Swedish academia who are at the level of PhD student or higher.
The applications are continuously evaluated throughout the year so it should be quick to get a decision.
Once you've decided on the size of your project, the next step asks you to choose a facility for the project.
Naturally you'll want to apply for the LUNARC projects.

##### Storage projects
Each user on Aurora gets 100GB of storage in their /home directory.
Should you need more space (very likely if working with imaging data) you can apply for a SNIC Storage project [here](https://supr.snic.se/round/storage/?).
The storage projects also come in three different sizes depending on your needs and the application procedure is very similar to the compute projects.
Note that you'll need to have a compute project at LUNARC to be able to use your storage.

#### Joining an existing project
You can also request to join an existing project. In the SUPR portal this option is found under **Projects -> Request Membership in Project**.
You can for example search for the project title or the name of the principal investigator.
Once you have found the project you want to join, press the **Request** button.
The PI of the project will have to accept your request.
You should get an email notice once this is done.

## LUNARC account
When you have been added to a project you can request LUNARC account in the SUPR portal.
This is done under **Accounts -> Account Requests -> Request LUNARC account**.
The username is typically formed from the three first letters of your first and last names, but you can also ask for a different username.
Once your request is handled you will receive an email with instructions on how to get your initial password.

To be able to log in to the LUNARC systems you'll need to set up the Pocket Pass authenticator app on your phone by following [this](https://lunarc-documentation.readthedocs.io/en/latest/authenticator_howto/) guide. Once this is done you should be able to connect to the Aurora HPC desktop by following [this](https://lunarc-documentation.readthedocs.io/en/latest/using_hpc_desktop/) guide.
