Medical License Validation Specification (MVLS)
===============================================


Version 0.0.3 (DRAFT)

First Published: December 31, 2013

Last Updated: March 11, 2014

Autorative URL: https://github.com/HHSIDEAlab/mlvs

_Comments and feedback are welcome._

Goals
-----

The goals of MVLS are the following:


* To define a common format for medical licenses (i.e. a standard code).
* To define a very simple and common way for medical license information to be
share as web-based resources. (i.e. an API)


Contents
--------


This repository contains both a technical specification and a reference
implementation that implements the specification.


Background
----------

The vision here is get license issuing authroities to publish information
in a uniform way.  To that end, this document desctribes very simple means for
doing so.


The first part of the specification that relates to the license `code`.  This is
a unique string for representing a particular license.  For example, MA-MDR-1234567
is a medical doctor in Massachusetts with the license number 1234567.


The second part of the specification defines a `URL` structure for pointing to
status information on particular license. For example
http://example.com/license/MA/MDR/1234567.json would point to information about
the medical doctor in Massachusetts with the license number 1234567. As you might
notice the `URL` contains the same the elements as the `code`. The first part is
the state, the second part is the license type, and the third part is the license
number (or identifier).  This is intentionaly structured in such a way
(using only HTTP GET) that the specification can be implemented using
content delivery networks. In other words, it is designed to be very simple and
inexpensive to implement.


Although this document is a draft, its contents are incorporated into the NPPES
Modernization effort.   In other words this specification is preciecely how the
NPPES redesign automaticaly validates licenses. See
https://github.com/HHSIDEAlab/npi or http://npi.io for more information.






The specification contains a startdard format for representing a medical license.


This document contains the specification itself followed by information on a reference implementation.



Medical License Verification Specification
==========================================


1. The Code
-----------


A medical license shall be represented as a string containing the following 3 items:

* The two-letter abbreviation code for state or US territory,
* The three-letter medial license type code as defined in `Medical License Universe CSV`. (See `docs` sub-folder within this repository)
* The license number or identifier.


These three items shall always be seperated by dashes.

Examples:

    MD-MDR-3001234   # Medical Doctor, license 3001234 in Maryland
    AK-DEN-829281    # Dentist license, 829281 in Arkansas
    CO-DOS-908232 # Doctor of Osteopathy, license 908232, in Colorado

Of course the format of the license number or identifier will vary by state and issuing body.



2 The URL (a RESTFul API)
-------------------------


The specification also defines RESTful protocol that can be implmented without
the need to write any software. Adherence of the specification can be achieved
by simply copying files to a web server with a predictable URL pattern.


The following text defines compliance with the URL specification.

* The server shall use HTTP as the transport protocol and the server shall resoind to HTTP GET.
* The resource shall employ SSL for encryption (HTTPS). Using HTTPS is used to mitigate the possibility of data tamprering in transit.
* The server shall implement a single URL with the following pattern: /license/[TWO-LETTER-STATE-CODE]/[THREE-LETTER-LICENSE-TYPE-CODE]/[LICENSE-NUMBER].json
* When a resource is found at the aformentioned URL, the HTTP response code 200 shall be returned.
* When a resource is found at the aformentioned URL, the response mimetype shall be "application/json".
* When a resource is found at the aformentioned URL, the response body shall contain a  single JSON object containg the following elements: "first\_name", "last\_name", "state", "license\_type", "number", "npi", "status", "created\_at", "updated\_at". "npi" is optional.  All other fields are required. Additional fields may be added to the object,  The order of fields is unimportant, hence a valid client reader should not rely on the ordering.  Exmplanations of each field follow below in the section titled, "More Details About the Response".
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
<td>first\_name</td>
<td>A string of the provider's First Name</td>
<td>Y</td>
</tr>

<tr>
<td>last\_name</td>
<td>A string of the provider's Last Name</td>
<td>Y</td>
</tr>

<tr>
<td>state</td>
<td>A two-letter string representing the state..  This filed shall onlyuse
offical two-letter abbreviations. See https://www.usps.com/send/official-abbreviations.htm </td>
<td>Y</td>
</tr>


<tr>
<td>credential</td>
<td>A text string describing the type of credential.<br></br>
For example, "Medial Doctor"</td>
<td>Y</td>
</tr>



<tr>
<td>license_type</td>
<td>A three-letter string containing a code resenting a license type.
Codes can be found in the document `ProviderLicenseUniverseFeb2014.csv` contained
in this repository.

Valid license_type examples include:<br></br> 
"MDR" (Medical Doctor)<br></br>
"DOS"(Doctor of Osteopathy)<br></br>
"PAS" (Physician Assistant)</td>
<td>Y</td>
</tr>

<tr>
<td>code</td>
<td>Concatenation of state code and license type code and the license number or identifier. Sperated by dashes.

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
Curl is just used as an example.  You could use many other tools or pretty
much any programming language.


Below is an example request using curl.  In this example, the server is
"somelicenseauthority.example.com", the state is "WV", the license type is MDR,
(Medical Doctor) and the license number is "234234534".

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

If we do the same thing again with the verbose "-v" option we can see the HTTP response code and the mimetype.

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


4. Reference Implemenation
--------------------------

The project contained within this GitHub repository is a reference implmentaion
of the specification.  It uses Django and can be deployed on almost any operating
system or web server.  The reference implementation is fully functional and
assumes one or several managers will manage the data.By default the underlying
database is SQLite, but this can be changed.


License records can be added and updated via Django's standard administrative interface
Default URL is `/admin`.


Here is how to get started. The instruction are meant to be executed inside a terminal.
The instructions assumes `python` and `pip` are already installed:

   git clone https://github.com/HHSIDEAlab/mlvs.git
   cd mlvs
   pip install -r mlvs/requirements.py
   python manage.py syncdb
   
When propted, say yes to create a super user so you can add licenses using the Django admin interface.
Then start the development server.

   python manage.py runserver

Point your browser to `http://127.0.0.1:8000`.  To get tot he admin, navigate to
http://127.0.0.1:8000/admin`.  Then look for 'Licenses' to view/add/edit/delete
Licenses.  the URL to server the licenses is as described in the specification
`[TWO-LETTER-STATE-CODE]/[THREE-LETTER-LICENSE-TYPE-CODE]/[LICENSE-NUMBER].json`

Read more about Django here: http://djangoproject.com


