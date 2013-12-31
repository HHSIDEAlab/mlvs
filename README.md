MVLS (DRAFT) 0.0.1
==================
_First Published December 31, 2013_

_Last Updated December 31, 2013_

MVLS refers to both a technical specification, "Medical License Verification Specification" and a system, "Medical License Verification System" that serves as a reference implementation for the Specification. Both the specification and system are described in this document.  This is a draft. Comments and feedback are welcome.

The goal of MVLS is to define a common way for medical license information to be stored so that it becomes trivial to determine a health providers license status. The specification is a RESTful protocol designed with simplicity in mind.  It is so simple in fact, that it can be implemented without the need to write any code.  It can be acheived simply by copying files to a web server with a predictable URL pattern.

This document will first describe the specification and then the system (Reference Implmentation).



Medical License Verification Specification
==========================================

To create a system that adheres to this specification shall:

* Use HTTP as the transport protocol and use the GET method.
* Use SSL for encryption (HTTPS). Using HTTPS is used to mitigate the possibility of data tamprering in transit.
* Implement a single URL with the following pattern: /license/[TWO-LETTER-STATE-CODE]/[LICENSE-NUMBER].json
* When a resource is found at the aformentioned URL, the HTTP response code 200 shall be returned.
* When a resource is found at the aformentioned URL, the response mimetype shall be "application/json".
* When a resource is found at the aformentioned URL, the response body shall contain a  single JSON object containg the following elements: "first\_name", "last\_name", "state", "license\_type", "number", "npi", "status", "created\_at", "updated\_at". "npi" is optional.  All other fields are required. Additional fields may be added to the object,  The order of fields is unimportant, hence a valid client reader should not rely on the ordering,  Exmplanations of each field follow below in the section titled, "More Details About the Response".
* When a resource is NOT found at the aformentioned URL, a non-200 HTTP status, such as 404 or 303 is returned. when the response code is 200, the response body and mime-type are irrelevant and can be ignored. It is presumed the license information is not available.


More Details About the Response
-------------------------------



<table>

<thead>
<tr>
<td>Field Name</td>
<td>Required</td>
<td>Details</td>
</tr>
</thead>

<tr>
<td>first\_name</td>
<td>Provider's First Name</td>
<td>Y</td>
</tr>

<tr>
<td>last\_name</td>
<td>Provider's Last Name</td>
<td>Y</td>
</tr>

<tr>
<td>state</td>
<td>Use only offical two-letter abbreviations. See https://www.usps.com/send/official-abbreviations.htm </td>
<td>Y</td>
</tr>

<tr>
<td>license\_type</td>
<td>A two-letter code presenting license type. Valid codes are:<br></br> 
"MD" (Medical Doctor)<br></br>
"DO"(Doctor of Osteopathy)<br></br> "PA" (Physician Assistant)</td>
<td>Y</td>
</tr>

<tr>
<td>number</td>
<td>The licanse number issued by the state</td>
<td>Y</td>
</tr>


<tr>
<td>npi</td>
<td>The National Provider Identifier (NPI) issued by CMS/NPPES</td>
<td>N</td>
</tr>

<tr>
<td>status</td>
<td>The status of the license. Valid codes are: <br></br>
     "ACTIVE" (Active) <br></br>
     "ACTIVE\_WITH\_RESTRICTIONS (Active with Restrictions) <br></br>
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

The examples below are demonstrated with "curl", a command-line web client that is installed on Mac OSX and Linux and can be downloaded for Windows.  Curl is just used as an example.  You could use many other tools or pretty much any programming language.


Below is an example request using curl.  In this example, the server is "somelicenseauthority.example.com", the sate is "WV", and the license number is "234234534".

    curl https://somelicenseauthority.example.com/license/WV/2342345345

The server responds with:

    {
    "first_name": "Foo",
    "last_name": "Bar",
    "state": "WV",
    "license_type": "MD",
    "number": "2342345345",
    "npi": "1223353456",
    "status": "ACTIVE",
    "created_at": "2013-12-30",
    "updated_at": "2013-12-30"
     }

If we do the same thing again with the verbose "-v" option we can see the HTTP response code and the mimetype.

    curl -v https://somelicenseauthority.example.com/license/WV/2342345345

Responds with

    ...
    < HTTP/1.0 200 OK
    ...
    < Content-Type: application/json
    ...
    {
        "first_name": "Foo",
        "last_name": "Bar",
        "state": "WV",
        "license_type": "MD",
        "number": "2342345345",
        "npi": "1223353456",
        "status": "ACTIVE",
        "created_at": "2013-12-30",
        "updated_at": "2013-12-30"
    * Closing connection #0
    }

Here is a negative example where the resource does not exist. We will use the "-I" flag to read the response head.

    curl -I https://somelicenseauthority.example.com/license/CA/999999999

This response means there is no medical license issued in CA with the number 999999999. The body if the response is unimportant.

    HTTP/1.0 404 NOT FOUND
    ...

Implementation Notes
--------------------

There are three ways to go about implementing this specification:
1. Create, and periodically update, the necessary JSON files and place them on any web server within a directory "license" and a subdirectory "[STATE]" where [STATE] is a a two letter abbreviation.  If you are only managing license for one state you would only have one subdirectory here.
2. Implement the above specification using any technology stack you like,
3. Use the free, open-source reference implementation described below.

Medical License Verification System
===================================

The project contained within this GitHub repository is a reference implmentaion of the specification.  It uses Django and can be deployed on almost any operating system or web server.  The reference implementation is fully functional and assumes one or several managers will manage the data.By default the underlying database is SQLite, but this can be changed.  Read more about Django here: http://djangoproject.com

License records can be added and updated via Django's standard administrative interface.

-ADD MORE DETAIL HERE-
