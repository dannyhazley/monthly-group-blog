"""
This will script the actual text of the email
It will apply formatting if possible and embed images
"""

from database_connection import read_group_and_blog_body, Group, BlogBody
import markdown

def get_all_recipients(group_id: Group) -> list[str]:
    emails: list[str] = []

    for member in group_id.group_members:
        emails.append(member.email)

    return emails

def process_body(all_blogs: list[BlogBody]) -> str:
    """
    Process header, then body, then image.  Add name in italics as "By ____" and then a divider line
    """
    formatted_body = f"#Your {all_blogs[0].month} Newsletter!\n"

    for blog in all_blogs:
        formatted_body += f"## {blog.header}\n"
        formatted_body += f"{blog.body}\n"
        formatted_body += f"![An image uploaded by {blog.name}]({blog.image})\n"
        formatted_body += f"_By {blog.name}_\n"
        formatted_body += "---\n"

    if formatted_body == f"#Your {all_blogs[0].month} Newsletter!\n":
        formatted_body = "# ERROR"

    html = markdown.markdown(formatted_body)
    return html

def write_email(group_id: str) -> tuple[list[str], str, str]:
    """
    Returns the email recipients, subject, and body
    """
    group, blog_body = read_group_and_blog_body(group_id)

    recipients = get_all_recipients(group)
    subject = "Your Monthly Group Blog"
    body = process_body(blog_body)

    return recipients, subject, body