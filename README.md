Medical License Validation Specification (MLVS)
===============================================

Version 0.0.5 (DRAFT)

_Created December 31, 2013_

_Updated: August 19, 2014_

URL: https://github.com/HHSIDEAlab/mlvs

Goals
-----

The goals of MVLS are to :

* Codify medical licenses (i.e. a standard coding convention).
* Define a web-based microservice convention to represent medical license status information at predectiable URLs.


This repository contains both a technical specification and two reference
implementations. The reference implementations are designed to help medical boards 
quickly and inexpensivley implement mlvs.

As noted this is a draft and CMS is interested in feedback from the community
and medical license organizations in particular. If your organization would like to pilot 
this functionality with CMS, as part of the NPPES Modernization Project (http://npi.io), please
email alan.viars AT cms.hhs.gov.

_Comments and feedback are welcome._


Understanding MLVS in 20 Seconds
--------------------------------

* Licensing organizations are identified by state and the type of license.
State is a two-letter code and license types are three-letter codes defined by CMS.   
This list can be found in this repository under the `docs` folder in CSV format.

* A coded license takes the form  `[STATE]-[LICENSE TYPE]-[NUMBER]` (e.g. DC-MDR-12345 
is a Medical Doctor (MDR) in the District of Columbia with a license number of 12345.

* The URL format similar but uses directy structure instead of dashes.
A license URL takes the form  `/license/[STATE]/[LICENSE_TYPE]/[NUMBER].json`
For example,  `https://example.com/license/MD/MDR/12345.json` is a Medical doctor (MDR)
in Maryland (MD) with a license number of 12345. The resouce at the URL is a simple, 
predictible structured document containing information about the license, most chiefly status
information.



Background
----------

The end goal here is to get license issuing authroities to publish information
in a uniform way.  To that end, this document describes very simple means for
doing so.


The first part of MLVS defines a license `code`.  This `code`
is a unique, predictable, string for representing a particular license.  For
example, `MA-MDR-1234567` is a medical doctor in Massachusetts with the
license number 1234567.


The second part of the specification defines a `URL` structure for pointing to
status information on particular license. For example
`https://example.com/license/MA/MDR/1234567.json`  points to information about
the medical doctor in Massachusetts with the license number 1234567. As you might
notice the `URL` contains the same the elements as the `code`. The first part is
the state, the second part is the license type, and the third part is the license
number (or identifier).  This is intentionally structured in such a way
(using only HTTP GET) that the specification can be implemented using
content delivery networks. In other words, it is designed to be very simple and
inexpensive to implement.


Although this document is a draft, its contents are incorporated into the NPPES
Modernization effort. In other words this specification is precisely how the
NPPES redesign automatically validates licenses. See
https://github.com/HHSIDEAlab/npi or http://npi.io for more information.



Medical License Verification Specification
==========================================


1. The Code
-----------

A string that adheres to the convention shall be formatted as follows:


    [TWO-LETTER-STATE-CODE]-[THREE-LETTER-LICENSE-TYPE-CODE]-[LICENSE-NUMBER]

where:

* [TWO-LETTER-STATE-CODE] is a two-letter abbreviation code for a US state or territory.
* [THREE-LETTER-LICENSE-TYPE-CODE] is a three-letter medial license type code.
For a complete list, see `USProviderLicenseTypesFeb2014.csv` in the `docs`
sub-folder within this repository)
*[LICENSE-NUMBER] is the license number or identifier.
* Two dashes (`-`) shall separate the three elements 


Examples:


    MD-MDR-3001234   # Medical Doctor, license 3001234 in Maryland
    AK-DEN-829281    # Dentist license, 829281 in Arkansas
    CO-DOS-908232    # Doctor of Osteopathy, license 908232, in Colorado

The format of the license number or identifier will vary by state and
issuing body.



2.1 The URL
------------

 The URL is in the following format.

     /license/[TWO-LETTER-STATE-CODE]/[THREE-LETTER-LICENSE-TYPE-CODE]/[LICENSE-NUMBER].json


2.2 Resource Response Details
-----------------------------

The specification also defines RESTful protocol that can be implemented without
the need to write any software. Adherence of the specification can be achieved
by simply copying files to a web server with a predictable URL pattern.


The following text defines compliance with the URL specification.

* The server shall use HTTP as the transport protocol and the server shall respond to HTTP GET.
* The resource shall employ SSL for encryption (HTTPS). Using HTTPS is used to mitigate the possibility of data tampering in transit.
* The server shall implement a single URL with the following pattern: /license/[TWO-LETTER-STATE-CODE]/[THREE-LETTER-LICENSE-TYPE-CODE]/[LICENSE-NUMBER].json
* When a resource is found at the aforementioned URL, the HTTP response code 200 shall be returned.
* When a resource is found at the aforementioned URL, the response mimetype shall be "application/json".
* When a resource is found at the aforementioned URL, the response body shall contain a single JSON object containg the following elements: "first\_name", "last\_name", "state", "license\_type", "number", "npi", "status", "created\_at", "updated\_at". "npi" is optional.  All other fields are required. Additional fields may be added to the object,  The order of fields is unimportant, hence a valid client reader should not rely on the ordering.  Explanations of each field follow below in the section titled, "More Details About the Response".
* When a resource is NOT found at the aformentioned URL, a non-200 HTTP status, such as 404 or 303 is returned. when the response code is 200, the response body and mime-type are irrelevant and can be ignored. It is presumed the license information is not available.


Details About the Response
--------------------------

<table>

<thead>
  <tr>
    <td>Field Name</td>
    <td>Details</td>
    <td>Required</td>
  </tr>
</thead>

<tr>
<td>first_name</td>
<td>A string of the provider's First Name</td>
<td>Y</td>
</tr>

<tr>
<td>last_name</td>
<td>A string of the provider's Last Name</td>
<td>Y</td>
</tr>

<tr>
<td>state</td>
<td>A two-letter string representing the state.  This filed shall onlyuse
offical two-letter abbreviations. See https://www.usps.com/send/official-abbreviations.htm </td>
<td>Y</td>
</tr>


<tr>
<td>credential</td>
<td>A text string describing the type of credential.<br></br>
For example, "Medial Doctor" for license_type "MDR"</td>
<td>Y</td>
</tr>



<tr>
<td>license_type</td>
<td>A three-letter string containing a code resenting a license type.
Codes can be found in the document `USProviderLicenseTypesFeb2014.csv` contained
in the docs folder of this repository.

Valid license_type examples include:<br></br> 
"MDR" (Medical Doctor)<br></br>
"DOS"(Doctor of Osteopathy)<br></br>
"PAS" (Physician Assistant)</td>
<td>Y</td>
</tr>

<tr>
<td>code</td>
<td>Implementation of part 1 of the MLVS specification. It is a concatenation of
state code, the license type code, and the license number or identifier. Sperated by dashes.

Valid code examples include:<br></br> 
"CA-MDR-12387123" (Medical Doctor) in California<br></br>
"VA-DOS-232859"(Doctor of Osteopathy) in Virginia<br></br>
"NY-PAS-98323" (Physician Assistant) in New York</td>
<td>Y</td>
</tr>



<tr>
<td>number</td>
<td>A string containing the license number issued by the issuing authority.</td>
<td>Y</td>
</tr>


<tr>
<td>npi</td>
<td>A string containing the National Provider Identifier (NPI) issued by CMS/NPPES.</td>
<td>N</td>
</tr>

<tr>
<td>status</td>
<td>A string containing the a code indicating the status of the license. Valid
codes are: <br></br>
     "ACTIVE" (Active) <br></br>
     "ACTIVE_WITH_RESTRICTIONS (Active with Restrictions) <br></br>
     "EXPIRED" (Expired) <br></br>
     "REVOKED" (Revoked) <br></br>
     "DECEASED" (Deceased) <br></br>
</td>
<td>Y</td>
</tr>

<tr>
<td>created_at</td>
<td>The date this record was first created. Format YYYY-MM-DD.</td>
<td>Y</td>
</tr>

<tr>
<td>updated_at</td>
<td>The date this record was last updated. Format YYYY-MM-DD.</td>
<td>Y</td>
</tr>


</table>



Examples
--------

The examples below are demonstrated with "curl", a command-line web client that
is installed on Mac OSX and Linux and can be downloaded for Windows.
Curl is just used as an example.  You could use many other tools or almost any
programming language.


In the curl example below, the server is
"somelicenseauthority.example.com", the state is "WV", the license type is MDR
(Medical Doctor), and the license number is "234234534".


    curl https://somelicenseauthority.example.com/license/WV/MDR/3242345345.json

The server responds with:

    { 
    "first_name": "Leonard",
    "last_name": "McCoy",
    "state": "WV",
    "license_type": "MDR",
    "credential": "Medical Doctor", 
    "code": "WV-MDR-3242345345",
    "number": "3242345345",
    "npi": "1323353456",
    "status": "ACTIVE",
    "issued_by": "West Virginia State Medical Board",
    "date_issued": "2010-12-30",
    "date_expires": "2015-12-30",
    "date_created": "2013-12-30",
    "date_updated": "2014-01-30"
     }

If we do the same thing again with the verbose "-v" option we can see the HTTP
response code and the mimetype.

    curl -v https://somelicenseauthority.example.com/license/CA/MDR/2342345345.json

Responds with

    ...
    < HTTP/1.0 200 OK
    ...
    < Content-Type: application/json
    ...
    {
        "first_name": "River",
        "last_name": "Song",
        "state": "CA",
        "license_type": "MDR",
        "credential": "Medical Doctor",
        "code": "CA-MDR-3242345345",
        "number": "2342345345",
        "npi": "1223353456",
        "status": "ACTIVE",
        "issued_by": "California State Medical Board",
        "date_issued": "2010-12-30",
        "date_expires": "2015-12-30",
        "date_created": "2013-12-30",
        "date_updated": "2014-01-30"
    }

Here is a negative example where the resource does not exist. We will use the
"-I" flag to just read the response head.

    curl -I https://somelicenseauthority.example.com/license/CA/DOS/999999999

This response means there is no DOS license (Doctor of Osteopathy) issued in CA
with the number 999999999. The body of the response is unimportant, since there
is no record.

    
    HTTP/1.0 404 NOT FOUND
    ...


3. Implementation Notes
-----------------------

There are three ways to go about implementing this specification:

1. _Upload Files to a Web Server_ - Create, and periodically update, the
necessary JSON files and place them on any web server within a directory
"license" and a subdirectory "[STATE]-[LICENSE-TYPE]" where [STATE] is a a
two letter abbreviation and [LICENSE-TYPE] is a three letter code corresponding
to a license type.  It is not necessary to stand up a dedicated web server to
implement this specification. You can use a content delivery network, such as
Amazon AWS S3, to implement this specification. The mention of S3 is provided as
an example, and should not be misconstrued as an endorsement.

2. _Roll Your Own_ - Implement the above specification using any technology stack
you like.

3. _Reference Implementation_ - Use the free, open-source reference
implementation described below.


4.  Reference Implemenation #1
------------------------------

The command line tool `csv2mlvs` converts a CSV file to a MLVS directory
structure decribed in the previous sections.  This script may be used to easily
create structure necessary so that all that is left to do is to upload the
structure to a web server or content delivery network.

This tool is part of `provider-data-tools`.  It can be installed using the
following command.


    pip install pdt

    csv2mlvs my.csv output

Where `my.csv` is a CSV containing provider data and `output` is the directory 
where output files and subdirectories are created. Upload the output to an
accesible web server. Using a CDN for this task is very inexpensive way to 
accomplish this.



Please see https://github.com/HHSIDEAlab/provider-data-tools for more
information.



5. Reference Implemenation #2
-----------------------------

The project contained within this GitHub repository is a full server reference
implementaion of the specification in Django.  It can be deployed on almost any
operating system or web server. By default the underlying
database is SQLite, but this can be changed.


License records can be added and updated via Django's standard administrative
interface. The default URL is `/admin`.


Here is how to get started. These instructions are meant to be executed inside a
terminal. These instructions assume `python` and `pip` are already installed:

   
   git clone https://github.com/HHSIDEAlab/mlvs.git
   cd mlvs
   pip install -r mlvs/requirements.py
   python manage.py syncdb
   
When prompted, say yes to create a super user so you can add licenses using the
Django admin interface. Then start the development server like so.


   python manage.py runserver

Point your browser to `http://127.0.0.1:8000`.  To get tot he admin, navigate to
http://127.0.0.1:8000/admin`.  Then look for 'Licenses' to view/add/edit/delete
Licenses.  the URL to server the licenses is as described in the specification
`[TWO-LETTER-STATE-CODE]/[THREE-LETTER-LICENSE-TYPE-CODE]/[LICENSE-NUMBER].json`

Read more about Django here: http://djangoproject.com
