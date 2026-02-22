INTRODUCTION
This project is an interactive NBA Sports Analytics Dashboard built using Streamlit. The dashboard analyzes NBA player performance through visualizations instead of raw statistics, making it easier to understand scoring trends, shooting efficiency, and overall player contributions such as assists and rebounds. The goal is to provide clear insights into player performance using real-world sports data.

The data used in this project is collected from the official NBA statistics using the NBA API (nba_api Python package).
This is real, publicly accessible data that reflects actual NBA player performance.

Dashboard Features
Bar Chart: Displays top scoring players based on total points
Histogram: Shows distribution of field goal shooting efficiency
Scatter Plot: Compares rebounds and assists with bubble size representing points
Heatmap: Shows correlation between key performance metrics

The dashboard is organized into two tabs:
Performance Overview – scoring and efficiency analysis
Advanced Correlation – relationships between different performance metrics
Additionally features includes,
sidebar filters, dropdown selection for teams, sliders for minimum points.

Data Update 
To update the dashboard for a new NBA season:
Change the season parameter in the API call inside the code
Reboot the Streamlit application
Because the data is fetched dynamically through an API, the dashboard can be easily maintained as a living analytical tool rather than a one-time project.

Deployment
The dashboard is deployed on Streamlit Community Cloud and is accessible through a public URL.
The GitHub repository contains all source code, the requirements.txt file, and this README documentation.

Conclusion
This project demonstrates how real NBA data can be transformed into meaningful insights using visual analytics. By combining multiple chart types, interactivity, the dashboard provides a clear and engaging way to evaluate NBA player performance.
