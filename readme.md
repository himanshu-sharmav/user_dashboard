    Categories: Four categories are defined in the BlogCategory model with choices: Mental Health, Heart Disease, Covid19, and Immunization.

    Blog Post Form: The BlogPostForm includes fields for Title, Image, Category, Summary, and Content. The Category field is a dropdown menu populated with the predefined categories.

    Draft Option: The is_draft field in the BlogPost model allows marking a blog post as a draft.

    Doctor Access: Doctors can create new blog posts using the create_blog_post view. They can also view their own blog posts in the dashboard.

    Patient Access: Patients can view all blog posts uploaded by doctors, categorized by their respective categories. This functionality is implemented in the dashboard view and dashboard.html template.

    Summary Truncation: The summary of each blog post displayed on the patient dashboard is truncated to 15 words with an ellipsis (...) at the end.