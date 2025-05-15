# Assisted by watsonx Code Assistant 
# Import necessary libraries
import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Spreadsheet Viewer", layout="wide")

# Display the main title
st.title("📊 Spreadsheet Viewer & Multi-Column Filter")

# Allow users to upload an Excel file
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xls"])

# Process the uploaded file if it exists
if uploaded_file is not None:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)

    # Display a success message
    st.success("File uploaded successfully!")

    # Display the full spreadsheet
    st.subheader("Full Spreadsheet View")
    st.dataframe(df, use_container_width=True)

    # Allow users to select columns for filtering
    selected_columns = st.multiselect("Select columns to filter", df.columns)

    # Initialize filters and match types dictionaries
    filters = {}
    match_type = {}

    # If columns are selected, display filter input fields
    if selected_columns:
        st.write("Set your filters:")
        for column in selected_columns:
            # Use columns and match type columns side by side
            col1, col2 = st.columns([3, 1])

            # Filter input field for the column
            with col1:
                filters[column] = st.text_input(f"Filter {column} (type value)")

            # Match type selection for the column
            with col2:
                match_type[column] = st.radio(
                    "Match Type",
                    ["Contains", "Exact"],
                    index=0,
                    key=f"match_{column}",
                    horizontal=True,
                )

    # Filter the data based on user input
    filtered_df = df
    for column, filter_value in filters.items():
        if filter_value:
            if match_type[column] == "Exact":
                filtered_df = filtered_df[filtered_df[column].astype(str).str.strip().eq(filter_value)]
            else:
                filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(filter_value, case=False, na=False)]

    # Display the filtered results
    st.subheader("Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

    # Allow users to download the filtered data as a CSV file
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download filtered data as CSV", csv, "filtered_data.csv", "text/csv")

# Display an info message if no file is uploaded
else:
    st.info("Please upload an Excel file to get started.")
