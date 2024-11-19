# autoMail

autoMail is a repository designed for automating the email-sending process using Google Sheets and custom templates. It provides a seamless way to send personalized emails to multiple recipients using their data stored in a Google Sheet. The repository contains two main directories: **google-sheet-auto** and **llm-custom-mail**, each offering unique functionality for crafting and sending emails.

---

## Directories and Their Functionalities

### **1. google-sheet-auto**
This directory allows you to send personalized emails using a pre-defined email template. 

#### **Features:**
- Connect to your Google Account and upload a Google Sheet containing:
  - Custom data.
  - Email IDs.
  - Row-specific values for each email.
- Define an email template with placeholders corresponding to column names in the Google Sheet.
- Automatically replace the placeholders in the template with the respective values for each email ID.
- Send personalized emails based on the template and row-specific data.

#### **How It Works:**
1. Upload a Google Sheet containing:
   - Email IDs in one column.
   - Additional columns for custom data (e.g., `Name`, `Order`, `Date`, etc.).
2. Write an email template such as:
3. The placeholders (`{{Name}}`, `{{Order}}`, `{{Date}}`) will be replaced with the corresponding values from each row in the Google Sheet.
4. Emails are sent to each recipient with their customized content.

---

### **2. llm-custom-mail**
This directory takes email customization a step further by leveraging a language model (LLM) to generate fully customized email content based on a user-defined prompt and placeholder values.

#### **Features:**
- Connect to your Google Account and upload a Google Sheet with:
- Custom data.
- Email IDs.
- Row-specific values for each email.
- Write a prompt explaining how to use placeholders to generate email content.
- Automatically replace placeholders with the respective values from each row.
- Send the modified data and prompt to the LLM, which generates personalized email content for each recipient.
- Send highly customized emails based on the generated content.

#### **How It Works:**
1. Upload a Google Sheet containing:
- Email IDs in one column.
- Additional columns for custom data (e.g., `Name`, `Feedback`, `Next Steps`, etc.).
2. Write a prompt such as:
3. The placeholders (`{{Name}}`, `{{Feedback}}`, `{{Next Steps}}`) are replaced with the respective row values.
4. The system sends the updated data and prompt to the LLM.
5. The LLM generates personalized email content tailored to each recipient's row data.
6. Emails are sent with the custom-generated content.

---

## Key Differences Between Directories
| **Feature**                  | **google-sheet-auto**                                | **llm-custom-mail**                                   |
|------------------------------|----------------------------------------------------|-----------------------------------------------------|
| **Template Type**             | Pre-defined email template with placeholders       | Prompt-based customization using LLM               |
| **Content Generation**        | Static placeholder replacement                     | Dynamic email generation via LLM                   |
| **Use Case**                  | Structured and consistent email format             | Highly personalized and adaptive email content     |

---

