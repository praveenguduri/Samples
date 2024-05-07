Intro:

"I've had the privilege of leading and contributing to transformative data initiatives across multiple organizations. At Discover Financial Services, I currently serve as a Senior Manager for Data Solutions, where I lead a talented team focused on building a robust data engineering organization. We've successfully implemented a data fabric that automates data pipelines for over 100 domains, significantly reducing data latency and expanding historical data accessibility.
Prior to this, at CNA Financial, I spearheaded a cloud data governance initiative, enhancing data quality and accelerating time-to-market by training users on cloud data governance practices. Additionally, I led the redesign of data engineering strategies, unifying data formats and models to drive significant fiscal improvements.
My journey in data engineering began at Discover Financial Services as a Principal Data Engineer, where I led the modernization of ETL processes, resulting in substantial cost savings and improved efficiency. I've also held roles at HMS Holdings and Infosys Ltd, where I led Hadoop platform rollouts, developed specialized input formats for various data sources, and implemented robust data quality frameworks.

What is DA to you

Data producers: These are the sources of your data, like sales transactions, customer clicks, or social media posts.
Data consumers: These are the people or applications that need to use the data to gain insights, like marketing teams, data analysts, or risk management departments.
Data architecture acts as a bridge between these three groups(Producer/Consumers and engineers). It defines how data is collected, stored, organized, and accessed.

Conflict resolution:
Situation: I was collaborating with a data producer team on the payments side. Their systems, running on PCF with an Oracle backend, weren't migrated to the cloud yet due to compliance concerns with storing card member data in clear text. We opted for Change Data Capture (CDC) to replicate data for analytics while on the legacy platform.
Challenge: To meet PCI guidelines requiring tokenization of sensitive data at rest, the team initially favored Transparent Data Encryption (TDE) over column-level tokenization using Protegrity. However, source teams were hesitant to share wallet keys used for TDE encryption due to security concerns under PCI.
Action: To address this conflict and find a viable solution, we took a proactive approach. We engaged in multiple discussions with the source teams to understand their concerns and constraints thoroughly. Recognizing the importance of compliance and security, we collaborated closely with security experts and sought guidance from a Qualified Security Assessor (QSA). This allowed us to develop a robust process for securely sharing encryption keys while ensuring compliance with PCI standards.Furthermore, we decided to showcase a Proof of Concept (POC) to demonstrate the effectiveness and security of the implemented solution. This not only helped alleviate concerns among stakeholders but also provided tangible evidence of our commitment to data security and compliance.

Question to build robust system:

What are the business questions we are trying to answer?
What would be the business impact of answering these questions?
What real-world behaviors do we need to record to help answer those questions?
What is the level of trust we need to have in the data?
How timely do we need the data to be?
Choosing framework -- how and why

How do you facilitate the prioritization of this framework?
How do you reduce the overhead of implementation?
How does the framework evolve over time?
How do you ensure the framework is not a one-way door and can be altered?
How do data, product, business, and software teams work together as a cohesive unit in this framework?
What happens if the data you need exists across teams?
How do you facilitate strong data modeling?
Choosing tech 
 When choosing technology for an organization or new data product, it's essential to select tools that enable the development team to ship outputs efficiently, allowing leaders to concentrate on outcomes and aligning outputs with desired results.
output refers to the act of shipping or delivering products to the market. While important, output alone does not guarantee success. On the other hand, outcome encompasses both output and user value. It emphasizes the importance of how the product is received and utilized by the end-user. Having an outcome mindset means focusing on the overall success of the product, rather than just its delivery.


I encountered a conflict with the Risk and Governance team regarding data lake curation. They advocated for mandatory metadata curation for all data attributes before making them available, aiming for a high level of data quality from the outset.
Understanding Their Concerns: While I appreciate their focus on data quality, I also understood the limitations of this approach. Curating 100% of the data upfront would significantly slow down the data science teams.
My Proposed Solution: I proposed a two-tiered approach:
Rapid Experimentation: For initial exploration and prototyping, data teams should have access to raw data from production with minimal restrictions. This allows for faster iteration and discovery of valuable insights that might otherwise be missed. Engineering teams should not be burdened with building elaborate pipelines for every experimental use case.
Data Promotion for Established Use Cases: Once a strong use case is identified, data consumers would be able to "promote" the data asset to a higher quality tier. This promotion process establishes the data as a "source of truth" for downstream applications. Future modifications should update this source instead of creating duplicate versions.
Balancing Agility and Governance: This approach balances the need for agile experimentation with the importance of data governance. It allows data scientists to explore the data freely while ensuring high-quality data for critical business applications.
Phased Governance: My approach advocated for applying data governance incrementally, focusing on high-impact use cases where it's most critical. This allows for a more adaptable approach that evolves alongside the data needs of the organization.
Communication and Change Management: To address concerns about data lineage and backward compatibility, I emphasized the importance of good communication between data producers and consumers. Producers could manage change communication through release notes and deprecation announcements, informing consumers of schema updates that might impact their workflows. Additionally, data assets that are no longer valuable should be retired, freeing up resources for producers to focus on actively used data products.
