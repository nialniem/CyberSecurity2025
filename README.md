# CyberSecurity2025
Project
https://github.com/nialniem/CyberSecurity2025	
installation instructions if needed
https://docs.djangoproject.com/en/3.1/intro/tutorial01/	

Flaw 1:
https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/	

In web applications, controlling access to unpublished or restricted content is essential for maintaining data integrity and user trust. In the Django polls application, a security flaw exists in the Results view, located at polls/view.py. This flaw allows users to access unpublished poll results by directly typing a URL that includes the polls ID and the results path. As a result, polls that are scheduled for future publication can be viewed prematurely, bypassing the intended access restrictions.

To fix this issue, a filter must be added to the Results view by overriding the get_queryset method. The following code demonstrates the solution: https://github.com/nialniem/CyberSecurity2025/blob/21086a820e146bf091dfd13d32c5862456f2356f/mysite/polls/views.py#L89-L91
def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

This method ensures that only polls with a publication date less than or equal to the current time are returned from the database. The filter() function applies a condition to the query, meaning that only rows meeting the specified criteria will be included in the result set. The pub_date__lte lookup restricts access to polls published in the past or present, while timezone.now() provides a timezone-aware current timestamp, preventing errors related to time zone differences.

Flaw 2:
https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/	

The risk is that the application exposes stack trace information and environment variables, making it easier for attackers to gather sensitive information and perform reconnaissance. The vulnerability was found in the Django project configuration file at https://github.com/nialniem/CyberSecurity2025/blob/8a4220e0517ff98dbd227547f2f15c51fd6edb64/mysite/mysite/settings.py#L26-L29 where the setting DEBUG = True was enabled. When debug mode is active, Django provides detailed error pages that include stack traces, file paths, server settings, and environment variables. While this information is useful during development, it becomes a serious security threat in a production environment. Attackers can use this exposed data to perform reconnaissance, identify system weaknesses, and plan more targeted attacks. Disabling debug mode prevents Django from displaying detailed error information to users. Instead, generic error pages are shown, which protect sensitive system details from public exposure. Additionally, custom error pages for HTTP status codes such as 404 (Page Not Found) and 500 (Internal Server Error) were added. These pages improve user experience while maintaining security by avoiding the disclosure of internal error data.

Flaw 3:
https://owasp.org/Top10/2025/A05_2025-Injection/	

An injection vulnerability is an application flaw that occurs when untrusted user input is sent directly to an interpreter, such as a database engine, without proper validation or escaping. This can cause the interpreter to execute parts of the user input as commands instead of treating them as normal data. One of the most common types is SQL injection, where attackers manipulate SQL queries to access or modify data in the database.In this application, a search function was implemented to allow users to find polls by their name. The vulnerable version of the code constructs an SQL query by concatenating user input directly into the SQL string. Because the user input is inserted into the query without sanitization or parameterization, an attacker can modify the structure of the SQL command.The condition OR 1 = 1 is always true, which causes the database to return all rows from the table instead of only the intended search results. To fix the code I put code that uses ORM query system to prevent user input from being interpreted as SQL code. https://github.com/nialniem/CyberSecurity2025/blob/8a4220e0517ff98dbd227547f2f15c51fd6edb64/mysite/polls/views.py#L38-L42
Flaw 4:
https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/	
In Django applications, the SECRET_KEY is an important cryptographic value used to secure several security mechanisms within the framework. Django uses this key to sign session cookies, generate CSRF tokens, and protect other sensitive data from tampering. Because of this, the key must remain secret and should never be publicly exposed. In this project, the SECRET_KEY was originally hardcoded in the settings.py file, which means anyone who has access to the source code could potentially see the key. If an attacker obtains this key, they may be able to forge signed cookies or manipulate other signed data, which could compromise the security of the application. To fix the code, the SECRET_KEY needs to be removed from the source code and loaded from an environment variable instead, so that the secret key is not exposed in the repository. During installation, the secret key is set in the system environment using the command (setx DJANGO_SECRET_KEY "django-insecure-dev-secret-key"). This ensures that the cryptographic key is not stored in the public repository and is instead provided securely when the application is installed or run.github.https://github.com/nialniem/CyberSecurity2025/blob/8a4220e0517ff98dbd227547f2f15c51fd6edb64/mysite/mysite/settings.py#L22-L24

Flaw 5:
https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/	
When an attacker is able to trick a system into recognizing an invalid or incorrect user as legitimate, this vulnerability is present. There may be authentication weaknesses if the application. Permits default, weak, or well-known passwords, such as "Password1" or "admin" username with an "admin" password. For example, a user account could be created using the password "12345", which is extremely weak and easy to guess. Allowing such weak passwords makes user accounts vulnerable to brute-force attacks and password guessing attacks. To fix the issue, password validation was added using Django’s built-in password validation system. The validate_password() function checks the strength of the password and prevents users from creating accounts with weak or commonly used passwords, improving the overall security of the authentication system. https://github.com/nialniem/CyberSecurity2025/blob/49433098bde39e1949a4ad074bde56a280848f35/mysite/polls/views.py#L18-L22


sources: 
https://learndjango.com/tutorials/customizing-django-404-and-500-error-pages	
https://docs.djangoproject.com/en/6.0/ref/models/querysets	
https://docs.djangoproject.com/en/6.0/topics/auth/passwords/#password-validation	
https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/		

