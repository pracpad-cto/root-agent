/**
 * Learning Portal - Configuration
 * 
 * This module provides application-wide configuration settings
 * including API endpoints, environment settings, and content parameters.
 * 
 * @author Abhijit Raijada
 * @designation Principle Engineer
 * @organization GRS
 */

/**
 * Configuration for the Learning Portal
 */

// API Configuration
const API_CONFIG = {
    development: {
        baseUrl: 'http://localhost:8000',  // Local development server
        timeout: 30000,  // 30 seconds
    },
    production: {
        baseUrl: 'https://te-demo-2d13023bc706.herokuapp.com',  // Production server
        timeout: 30000,
    }
};

// Set the current environment
const CURRENT_ENV = 'production';  // Change to 'production' for production deployment

// Export API configuration
const API_BASE_URL = API_CONFIG[CURRENT_ENV].baseUrl;
const API_TIMEOUT = API_CONFIG[CURRENT_ENV].timeout;

// Module Configuration
const moduleConfig = {
    module1: {
        name: 'Assessment Framework',
        units: {
            unit1: {
                title: 'OpEx vs. CapEx',
                description: 'Complete the following questions to test your understanding.',
                questions: [
                    {
                        text: "In your organization, how are technology investments typically categorized into OpEx and CapEx? How does this categorization impact the company's financial strategies? ",
                        type: "open",
                        guide: "Learners are encouraged to reflect on how their companies manage technology investments and whether the current strategies align with their company’s financial goals."
                    },
                    {
                        text: "Describe a scenario where your organization faced a decision between choosing an OpEx or CapEx approach. What were the financial and strategic outcomes of that decision?",
                        type: "open",
                        guide: "Learners can reflect on real-life decision-making processes and their outcomes in their professional settings, helping to tie theory with practice"
                    },
                    {
                        text: "How would you advise a technology start-up that has limited cash flow but needs to invest in IT infrastructure? Should they prioritize OpEx or CapEx, and why?",
                        type: "open",
                        guide: "This encourages learners to think critically about different financial approaches based on the type and size of the company, providing room for applied knowledge. "
                    },
                    {
                        text: "How do you foresee the evolution of cloud-based services impacting companies' financial strategies?",
                        type: "open",
                        guide: "This question encourages learners to think about future trends in technology economics and the growing influence of cloud-based technologies on financial strategies. "
                    },
                    {
                        text: "How can the balance between OpEx and CapEx influence the ability of a company to innovate or scale its technology infrastructure? ",
                        type: "open",
                        guide: "Learners are asked to consider the broader implications of financial management on a company’s ability to remain competitive and adaptive in a tech-driven landscape."
                    }
                ]
            },
            unit2: {
                title: 'CapEx: A Deeper Dive',
                description: 'Complete the following questions to test your understanding.',
                questions: [
                    {
                        text: "How does your organization plan and approve CapEx projects, and what are the key challenges in obtaining approval for major technology investments?",
                        type: "open",
                        guide: "Reflect on how CapEx proposals are evaluated and approved in your company. Consider the steps involved, the stakeholders, and any challenges faced during the approval process."
                    },
                    {
                        text: "Describe a situation where your organization used depreciation to manage a significant CapEx investment. What method was used, and how did it affect financial statements over time?",
                        type: "open",
                        guide: "Think about a time when your company managed a significant CapEx investment using a specific depreciation method. How did it influence cash flow and financial reporting over the years? "
                    },
                    {
                        text: "If you were responsible for recommending a CapEx project for your organization, what approach would you take to determine the appropriate depreciation method? ",
                        type: "open",
                        guide: "Reflect on the factors you would consider in recommending a specific depreciation method. Would you choose straight-line or declining balance, and why? "
                    },
                    {
                        text: "How does your company balance CapEx investments with the ongoing costs of maintaining operational efficiency? What challenges do you face in achieving this balance? ",
                        type: "open",
                        guide: "Consider how your organization manages both CapEx and OpEx, and how this balance affects the company’s financial stability and long-term growth. "
                    },
                    {
                        text: "How might changes in depreciation policies affect your company’s decision to invest in new technology infrastructure? ",
                        type: "open",
                        guide: "Think about how a change in depreciation policies could impact the planning and approval of CapEx projects in your company. Would it make investments more or less attractive? "
                    },
                    {
                        text: "In your opinion, what are the strategic advantages of using CapEx to invest in in-house technology infrastructure instead of relying on OpEx models like cloud services?",
                        type: "open",
                        guide: "Reflect on the potential benefits and drawbacks of CapEx investments in in-house technology infrastructure versus OpEx options like cloud services, and consider how these choices align with long-term strategic goals"
                    },
                    {
                        text: "Consider a CapEx project you have encountered in your organization. How did the approval process impact the timeline and ultimate success of the project? ",
                        type: "open",
                        guide: "Think about how the CapEx approval process influenced the success or failure of a project. Was it delayed due to stakeholder concerns, or was it expedited because of clear alignment with strategic goals? "
                    },
                    {
                        text: "How does the selection of depreciation methods impact the perceived value of CapEx investments among stakeholders? ",
                        type: "open",
                        guide: "Reflect on how different depreciation methods might influence the perception of an asset's value for stakeholders, and how this affects decision-making regarding CapEx projects "
                    },
                    {
                        text: "How could improved visibility of CapEx depreciation curves enhance your company’s financial planning and decision-making processes?",
                        type: "open",
                        guide: "Consider how a clearer understanding of depreciation curves might provide better insights for long-term planning, such as replacement cycles, cash flow projections, and future technology investments. "
                    },
                    {
                        text: "What steps could your organization take to more effectively communicate CapEx proposals and their financial impact to stakeholders?",
                        type: "open",
                        guide: "Reflect on the ways in which CapEx proposals are presented within your organization. Are there improvements that could be made in terms of presentation, metrics, or clarity to secure faster approval?  "
                    }
                ]
            },
            unit3: {
                title: 'Understanding Depreciation ',
                description: 'Complete the following questions to test your understanding.',
                questions: [
                    {
                        "text": "How does your organization currently apply depreciation to its assets, and what challenges are faced in selecting the appropriate method?",
                        "type": "open",
                        "guide": "Reflect on the process of choosing a depreciation method for different assets in your organization. Who is involved in these decisions, and what factors influence the choice of method? "
                    },
                    {
                        "text": "Describe a situation where the depreciation method used impacted your organization's financial planning or strategic decisions.",
                        "type": "open",
                        "guide": "Think of a time when the chosen depreciation method, such as straight-line or declining balance, significantly influenced financial reporting, cash flow, or resource allocation in your company."
                    },
                    {
                        "text": "If you were responsible for recommending a depreciation method for a new technology investment, which method would you choose and why?",
                        "type": "open",
                        "guide": "Reflect on the considerations you would take into account, such as the type of asset, its expected usage, and the financial goals of your organization. Would you opt for straight-line, declining balance, or units of production, and why? "
                    },
                    {
                        "text": "How does depreciation impact the perceived value of your company’s assets on the balance sheet?",
                        "type": "open",
                        "guide": "Consider how accumulated depreciation affects the net book value of assets and the way stakeholders perceive the financial health of your organization. "
                    },
                    {
                        "text": "In what ways does the selection of a depreciation method influence your company's income statement and tax obligations?",
                        "type": "open",
                        "guide": "Think about situations where depreciation is directly linked to asset usage, such as production hours or output. How does this help in accurately reflecting the wear and tear of assets in your financial statements?  "
                    },
                    {
                        "text": "How does the units of production depreciation method benefit your company’s approach to aligning asset usage with expenses?",
                        "type": "open",
                        "guide": "Learners should consider how this method ties depreciation directly to asset usage, such as production hours or units produced, providing a more accurate reflection of wear and tear in financial statements. They can discuss its benefits in managing manufacturing or service equipment costs."
                    },
                    {
                        "text": "How might changes in your organization's depreciation policies affect cash flow and future investment decisions?",
                        "type": "open",
                        "guide": "Reflect on how altering depreciation methods or useful life estimates could impact cash flow from operations and influence decisions regarding future capital investments. "
                    },
                    {
                        "text": "In your opinion, what are the strategic advantages of using accelerated depreciation methods, like declining balance, for technology assets?",
                        "type": "open",
                        "guide": "Consider how accelerated depreciation might benefit your organization in terms of tax savings, asset replacement cycles, or keeping pace with technological changes. "
                    },
                    {
                        "text": "How does depreciation as a non-cash expense affect your company’s cash flow statement, and why is it important to add it back to net income?",
                        "type": "open",
                        "guide": "Reflect on the significance of depreciation being added back to net income in the cash flow statement and how it impacts the true cash-generating ability of your organization. "
                    },
                    {
                        "text": "What factors would you consider when determining the useful life of a new technology asset in your organization?",
                        "type": "open",
                        "guide": "Think about the various aspects that influence the determination of an asset's useful life, such as technological obsolescence, maintenance practices, and the asset’s expected contribution to business operations. "
                    }
                ]
            },
        }
    },
    module2: {
        name: "Advanced Assessment",
        description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: "Exit Run Rate or Zero Balance Basis",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "In your organization, how are budgeting decisions made regarding the use of Exit Run Rate versus Zero Balance Budgeting? How do these decisions impact financial forecasting and operational stability?",
                        "type": "open",
                        "guide": "Reflect on how your organization approaches these budgeting methods. Consider how these decisions align with financial stability and support strategic goals."
                    },
                    {
                        "text": "Describe a scenario where your organization had to choose between using Exit Run Rate or Zero Balance Budgeting for managing a project. What were the key factors that influenced the decision, and what were the outcomes?",
                        "type": "open",
                        "guide": "Think about a real-world decision involving budgeting methods and reflect on how the choice affected project execution and financial planning."
                    },
                    {
                        "text": "If you were advising a technology company with significant ongoing operational costs, would you recommend Exit Run Rate or Zero Balance Budgeting to manage those costs? Why?",
                        "type": "open",
                        "guide": "This encourages you to think critically about how budgeting methods can support a company’s unique needs, especially in managing recurring operational expenses."
                    },
                    {
                        "text": "How can the use of Zero Balance Budgeting foster cost control and innovation in technology projects?",
                        "type": "open",
                        "guide": "Consider how this method can drive efficiency and ensure that investments align with strategic objectives, eliminating unnecessary expenses."
                    },
                    {
                        "text": "In what ways can Exit Run Rate budgeting be beneficial for organizations looking to maintain consistency in their operational costs?",
                        "type": "open",
                        "guide": "Reflect on how Exit Run Rate can help manage stability in financial planning, ensuring that recurring expenses are predictable and manageable over time."
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: "Strategic Planning ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "In your organization, how are budgeting decisions made regarding the use of Exit Run Rate versus Zero Balance Budgeting? How do these decisions impact financial forecasting and operational stability?",
                        "type": "open",
                        "guide": "Reflect on how your organization approaches these budgeting methods. Consider how these decisions align with financial stability and support strategic goals."
                    },
                    {
                        "text": "Describe a scenario where your organization had to choose between using Exit Run Rate or Zero Balance Budgeting for managing a project. What were the key factors that influenced the decision, and what were the outcomes?",
                        "type": "open",
                        "guide": "Think about a real-world decision involving budgeting methods and reflect on how the choice affected project execution and financial planning."
                    },
                    {
                        "text": "If you were advising a technology company with significant ongoing operational costs, would you recommend Exit Run Rate or Zero Balance Budgeting to manage those costs? Why?",
                        "type": "open",
                        "guide": "This encourages you to think critically about how budgeting methods can support a company’s unique needs, especially in managing recurring operational expenses."
                    },
                    {
                        "text": "How can the use of Zero Balance Budgeting foster cost control and innovation in technology projects?",
                        "type": "open",
                        "guide": "Consider how this method can drive efficiency and ensure that investments align with strategic objectives, eliminating unnecessary expenses."
                    },
                    {
                        "text": "In what ways can Exit Run Rate budgeting be beneficial for organizations looking to maintain consistency in their operational costs?",
                        "type": "open",
                        "guide": "Reflect on how Exit Run Rate can help manage stability in financial planning, ensuring that recurring expenses are predictable and manageable over time."
                    }
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: "Run vs. Change",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "In your organization, how are budgeting decisions made regarding 'Run' versus 'Change' activities? How do these decisions impact operational efficiency and strategic innovation? ",
                        "type": "open",
                        "guide": "Reflect on how your organization allocates resources to support both day-to-day activities ('Run') and initiatives that drive growth and transformation ('Change'). Consider the implications of these decisions on both current stability and future strategic goals. "
                    },
                    {
                        "text": "Describe a scenario where your organization had to decide between investing in operational efficiency ('Run') or pursuing innovation and growth ('Change'). What factors influenced the decision, and what were the outcomes?",
                        "type": "open",
                        "guide": "Think about a real-world decision that involved allocating resources towards either operational activities or innovative projects. Reflect on how the decision impacted business performance and the ability to innovate"
                    },
                    {
                        "text": "If you were advising a technology company facing challenges in maintaining its current operations while also trying to innovate, how would you recommend balancing 'Run' and 'Change' budgeting? Why? ",
                        "type": "open",
                        "guide": "Consider how balancing operational stability with transformative initiatives can help an organization adapt to market conditions while staying competitive. Think about how resource allocation should align with both immediate needs and strategic opportunities."
                    },
                    {
                        "text": "How can adopting a dynamic budgeting approach help your organization manage 'Run' and 'Change' activities more effectively? ",
                        "type": "open",
                        "guide": "Reflect on the benefits of flexible budgeting that allows for adjustments in resource allocation throughout the year. Consider how this approach can help the organization respond to emerging opportunities or market shifts. "
                    },
                    {
                        "text": "In what ways can a portfolio management approach assist in balancing operational efficiency with strategic growth? ",
                        "type": "open",
                        "guide": "Reflect on how categorizing projects based on their potential impact and risk can help your organization allocate resources more effectively. Consider how a balanced portfolio approach can support both maintaining current systems and investing in new opportunities for future success. "
                    }
                ]
            },
            unit4: {
                name: "Advanced Assessment",
                title: "Budget Plugs",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "Describe a scenario where your organization had to use a budget plug to bridge a financial shortfall. What factors led to the gap, and how was the plug used to address it? What were the outcomes? ",
                        "type": "open",
                        "guide": "Think about a specific instance where unforeseen expenses or revenue changes required the use of a budget plug. Reflect on how the decision affected the overall financial health and progress of the organization. "
                    },
                    {
                        "text": "If you were advising a company experiencing frequent budget gaps, how would you recommend using budget plugs responsibly while maintaining financial accuracy? Why? ",
                        "type": "open",
                        "guide": "Consider how strategic use of budget plugs can help cover financial shortfalls without compromising transparency. Think about the importance of balancing short-term adjustments with the need for accurate financial reporting and long-term stability. "
                    },
                    {
                        "text": "How can scenario planning and rolling forecasts help manage budget plugs more effectively in your organization? ",
                        "type": "open",
                        "guide": "Reflect on the benefits of using scenario planning and rolling forecasts to continuously adapt budget plugs based on updated information. Consider how these approaches can enhance both proactive decision-making and financial accuracy"
                    },
                    {
                        "text": "In what ways can understanding the risks and benefits of budget plugs help your organization use them effectively in financial planning? ",
                        "type": "open",
                        "guide": "Reflect on the potential advantages of budget plugs, such as flexibility and adaptability, and the associated risks, like over-reliance or financial misrepresentation. Consider how a thorough understanding of both can guide responsible and strategic use of budget plugs to support overall financial health. "
                    }
                ]
            },
            unit5: {
                name: "Advanced Assessment",
                title: "Initiative/Project Planning",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "Describe a scenario where your organization had to use a specific project budgeting technique (e.g., zero-based or incremental budgeting) for a major initiative. What factors led to choosing this technique, and how did it impact project outcomes? ",
                        "type": "open",
                        "guide": "Think about a specific project where you applied a particular budgeting approach. Reflect on why that approach was selected, considering the project’s complexity and strategic importance. Discuss how it influenced the project’s financial efficiency and overall success.  "
                    },
                    {
                        "text": "if you were advising a company on resource allocation for a major project, how would you prioritize resource distribution to ensure the project's success while managing costs effectively? Why? ",
                        "type": "open",
                        "guide": "Consider how identifying critical resources—such as human, financial, or material—and prioritizing them strategically can impact the project's outcomes. Reflect on how effective resource allocation helps in achieving project objectives without overextending budgets.  "
                    },
                    {
                        "text": "How can cost estimation techniques such as analogous estimation or parametric estimation help improve budgeting accuracy for large-scale projects in your organization? ",
                        "type": "open",
                        "guide": "Reflect on the benefits of different cost estimation techniques, such as using historical data or statistical models to forecast project costs. Think about how these methods can enhance the reliability of your project budget and help manage uncertainties. "
                    },
                    {
                        "text": "In what ways can monitoring and controlling project budgets, such as using budget tracking tools or variance analysis, support effective project management in your organization?  ",
                        "type": "open",
                        "guide": "Reflect on how regular budget tracking and variance analysis contribute to project success by providing timely insights into budget adherence. Consider how these techniques ensure transparency and enable proactive adjustments to keep the project on track.  "
                    }
                ]
            },
            unit6: {
                name: "Advanced Assessment",
                title: "Project Funding (Project “Wallets”) ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "Describe a scenario where your organization had to utilize project wallets to manage multiple initiatives simultaneously. How did this impact financial oversight and project success?  ",
                        "type": "open",
                        "guide": "Think about a time when allocating funds from a project wallet helped balance competing initiatives. Reflect on how this decision influenced the overall financial discipline and project outcomes. "
                    },
                    {
                        "text": "If you were advising a company facing challenges in managing project funding, how would you recommend using internal and external funding sources effectively?  ",
                        "type": "open",
                        "guide": "Consider how a combination of internal capital allocations and external funding options, such as venture capital or grants, could support strategic projects without compromising financial sustainability.  "
                    },
                    {
                        "text": "How can hybrid funding models help manage financial risks in your organization?  ",
                        "type": "open",
                        "guide": "Reflect on the benefits of blending internal and external funding to optimize resource allocation and mitigate financial risks. Consider how this approach could enhance your organization's ability to respond to changing project needs and market dynamics. "
                    },
                    {
                        "text": "In what ways can understanding the advantages and challenges of using project wallets support your organization’s strategic initiatives ",
                        "type": "open",
                        "guide": " Reflect on how project wallets contribute to transparency, financial accountability, and strategic alignment within an organization. Consider how a thorough understanding of funding mechanisms and governance can enhance decision-making for key projects. "
                    }
                ]
            }
        }
    },
    module3: {
        name: "Advanced Assessment",
        description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: "Balance Sheets and General Ledger",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How might you use the Balance Sheet to evaluate your organization’s capacity to take on a new technology initiative? ",
                        "type": "open",
                        "guide": "Consider whether your company’s current assets and liabilities provide the flexibility needed for a major new project. Reflect on how assessing liquidity and solvency can shape your technology strategy decisions. "
                    },
                    {
                        "text": "In what ways can the General Ledger be useful in identifying risks and opportunities in ongoing technology projects?",
                        "type": "open",
                        "guide": "Think about how a detailed understanding of revenue and expenditure trends, as captured in the General Ledger, could reveal areas of overspending, potential for resource reallocation, or opportunities for improving project performance. "
                    },
                    {
                        "text": "How do the Balance Sheet and General Ledger complement each other when making strategic technology decisions? ",
                        "type": "open",
                        "guide": "Reflect on how the Balance Sheet provides a snapshot of financial stability, while the General Ledger offers more granular insights. How might combining these tools help you make a more well-rounded decision regarding technology investments or strategic initiatives? ."
                    },
                    {
                        "text": "How would you apply the concepts learned about these financial tools to help prioritize projects within your organization? ",
                        "type": "open",
                        "guide": "Consider how the data provided by these documents might help you determine which technology projects to prioritize, whether based on available capital, risk mitigation, or alignment with broader organizational goal"
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: "Forecasting, Planning, and Budgeting as Strategic Tools for Technology Projects",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How would you use forecasting, planning, and budgeting differently in your current role?",
                        "type": "open",
                        "guide": "Consider the unique needs and challenges of your organization. How could financial forecasting help predict market opportunities or risks? How could strategic planning align your team's activities with company objectives? And finally, how could effective budgeting help you ensure the efficient allocation of resources?"
                    },
                    {
                        "text": "Which aspect—forecasting, planning, or budgeting—do you feel most confident in applying? Why?",
                        "type": "open",
                        "guide": "Reflect on your strengths and previous experience in these areas. Which activity do you find easiest to apply, and which one requires more practice? "
                    },
                    {
                        "text": "Think about a recent project in your organization—how did forecasting, planning, or budgeting impact its outcome?",
                        "type": "open",
                        "guide": "Reflect on a recent initiative. Did you face unexpected financial challenges? Could more effective forecasting have helped anticipate them? Did planning provide a clear roadmap for execution, and did budgeting provide adequate resources to stay on track?."
                    }                        
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: "Cost Allocation: Funding Cost Centers vs. Profit Centers",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How would you explain the distinction between a cost center and a profit center? ",
                        "type": "open",
                        "guide": "Reflect on the distinct roles each type of center plays within an organization—cost centers focus on maintaining operational efficiency and supporting essential services, while profit centers drive revenue generation and strategic growth. How do these differences shape their contributions to organizational success? "
                    },
                    {
                        "text": "What factors would influence your decision when allocating funding between cost centers and profit centers?",
                        "type": "open",
                        "guide": "Consider the need to balance operational stability with revenue-generating initiatives. How would factors such as organizational priorities, immediate operational needs, and long-term growth goals impact your allocation decisions? "
                    },
                    {
                        "text": "Which cost allocation method—traditional allocation, activity-based costing (ABC), or zero-based budgeting (ZBB)—would best align with your organization's strategy, and why?",
                        "type": "open",
                        "guide": "Based on your knowledge of your organization’s financial structure and goals, evaluate the strengths and limitations of each method. Which approach would ensure the most effective use of resources? "
                    },
                    {
                        "text": "Why is funding cost centers critical for the long-term sustainability of your organization?",
                        "type": "open",
                        "guide": "Discuss how ensuring adequate resources for cost centers, such as IT and HR, supports operational stability and provides the foundation for organizational productivity and success. How does this enable other departments to achieve their objectives?"
                    },
                    {
                        "text": "How does strategic funding of profit centers contribute to business growth and innovation",
                        "type": "open",
                        "guide": "Reflect on the role of profit centers in driving revenue, fostering innovation, and achieving market competitiveness. How can targeted investments in profit centers support your organization’s strategic goals?  "
                    }            
                ]
            }
        }
    },
    module4: {
        name: "Advanced Assessment",
        description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: "Virtual Machines ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "Describe a scenario where your organization leveraged Virtual Machines (VMs) to enhance operational flexibility. How did this impact resource optimization and cost efficiency?  ",
                        "type": "open",
                        "guide": "Reflect on how using VMs allowed your organization to consolidate servers or manage workloads more effectively. Consider the impact this had on reducing physical hardware costs and increasing operational efficiency.  "
                    },
                    {
                        "text": "If you were advising a company transitioning from physical servers to Virtual Machines, how would you recommend scaling their VM environment effectively? ",
                        "type": "open",
                        "guide": "Think about techniques such as dynamic resource allocation and predictive scaling. Reflect on how these strategies could ensure seamless scaling while maintaining performance and resource efficiency.  "
                    },
                    {
                        "text": "How can Virtual Machines support your organization’s disaster recovery plan? ",
                        "type": "open",
                        "guide": "Reflect on the role of VMs in creating system replicas and enabling rapid recovery. Consider how this approach could minimize downtime and ensure business continuity during unexpected disruptions. "
                    },
                    {
                        "text": "In what ways can Virtual Machines contribute to your organization’s strategic growth and innovation? ",
                        "type": "open",
                        "guide": "Reflect on how VMs can facilitate development and testing environments, enable faster deployment of new applications, and support cutting-edge technologies. Consider the financial and operational advantages this provides for strategic initiatives. "
                    },
                    {
                        "text": "How does understanding the scalability and management of Virtual Machines influence your organization’s approach to IT infrastructure?  ",
                        "type": "open",
                        "guide": "Reflect on the importance of managing VM environments effectively, including resource allocation and cost monitoring. Consider how this understanding aligns with long-term goals for operational sustainability and technological advancement.  "
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: "Storage – SAN vs. NAS ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How can implementing a SAN or NAS benefit your organization’s data management strategy? ",
                        "type": "open",
                        "guide": "Reflect on how SAN can enhance scalability, performance, and reliability for mission-critical applications.Consider how NAS can improve file accessibility, collaboration, and remote access while providing cost-effective storage.Identify specific areas where SAN or NAS could address your organization’s current storage challenges. "
                    },
                    {
                        "text": "What are the key differences between SAN and NAS, and how do these differences impact your organization’s storage needs? ",
                        "type": "open",
                        "guide": "Compare SAN’s high-speed block-level storage with NAS’s file-sharing capabilities.Consider SAN’s role in virtualization and high-performance computing versus NAS’s role in centralized file storage and backup solutions.Evaluate which solution aligns better with your organization’s data access, scalability, and security requirements. "
                    },
                    {
                        "text": "How do SAN and NAS contribute to disaster recovery and business continuity in a data-driven enterprise? ",
                        "type": "open",
                        "guide": "Consider how SAN supports real-time data replication and high-availability storage architectures.Evaluate how NAS offers automated backups, snapshots, and cloud integration to prevent data loss.Reflect on how both technologies help organizations recover quickly from system failures or cyber threats. "
                    }, 
                    {
                        "text": "If tasked with planning a SAN or NAS implementation, what factors would you prioritize to ensure a successful deployment? ",
                        "type": "open",
                        "guide": "For SAN, consider factors like scalability, cost, network infrastructure (Fibre Channel or iSCSI), and application workload requirements.For NAS, evaluate file access needs, user permissions, remote access, and cloud integration.Identify key security measures, backup strategies, and long-term maintenance considerations for both solutions."
                    }, 
                    {
                        "text": "What role do SAN and NAS play in supporting mission-critical applications within large-scale enterprises? ",
                        "type": "open",
                        "guide": "Think about how SAN delivers the high-speed, low-latency storage required for databases, financial transactions, and virtualization.Consider how NAS provides structured data storage for media production, document management, and remote collaboration.Reflect on how a hybrid SAN-NAS approach could enhance both performance and accessibility in your organization’s IT strategy? "
                    }                           
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: "Mainframe Computing",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do mainframes continue to be a critical part of modern enterprise IT?",
                        "type": "open",
                        "guide": "Reflect on the key benefits of mainframes, including high availability, security, and processing power.Consider why industries like finance, healthcare, and government still rely on mainframes despite the rise of cloud computing."
                    },
                    {
                        "text": "When should an organization choose mainframes over cloud computing?",
                        "type": "open",
                        "guide": "Identify specific scenarios where mainframes provide superior performance, such as real-time transaction processing and regulatory compliance.Think about your own industry—are there mission-critical workloads that would benefit from mainframe infrastructure? "
                    },
                    {
                        "text": "How does modernizing mainframe environments improve efficiency and cost management?",
                        "type": "open",
                        "guide": "Reflect on strategies like AI-driven automation, containerization, and hybrid cloud integration in mainframe environments.How could these modernization efforts reduce operational expenses (OpEx) while maintaining system efficiency? "
                    },
                    {
                        "text": "What are the key differences between horizontal and vertical scaling in mainframes?",
                        "type": "open",
                        "guide": "Compare the advantages of horizontal scaling (adding more nodes for workload distribution) and vertical scaling (upgrading a single system’s CPU and memory).Consider how scalability strategies impact enterprise performance and long-term IT investments. "
                    },
                    {
                        "text": "How can enterprises effectively integrate mainframes into a hybrid cloud strategy?",
                        "type": "open",
                        "guide": "Reflect on how hybrid cloud models balance cost, security, and performance by keeping mission-critical workloads on mainframes while leveraging cloud computing for other tasks.How can your organization apply hybrid cloud strategies to optimize IT infrastructure and enhance agility? "
                    }            
                ]
            },
            unit4: {
                name: "Advanced Assessment",
                title: "Cloud Computing ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How have the different models of cloud computing (IaaS, PaaS, SaaS) transformed IT operations in enterprises",
                        "type": "open",
                        "guide": "think about the distinct functionalities of each cloud model and how they align with various organizational needs. Reflect on how these models can streamline processes, enhance scalability, and reduce operational overhead in your organization. "
                    },
                    {
                        "text": "Which benefits of cloud computing are most impactful for your organization, and how do they align with strategic goals? ",
                        "type": "open",
                        "guide": "identify key advantages, such as cost savings, flexibility, or improved collaboration. Reflect on how these benefits support your organization’s objectives for growth, innovation, and competitiveness"
                    },
                    {
                        "text": "What challenges associated with cloud computing are most relevant to your industry, and how can they be addressed?",
                        "type": "open",
                        "guide": "Consider obstacles like data security, compliance, or integration complexities. Reflect on strategies your organization can adopt to mitigate these challenges and maximize the value of cloud adoption. "
                    },
                    {
                        "text": "How can cloud deployment strategies (public, private, hybrid, multi-cloud) support your organization’s unique IT needs? ",
                        "type": "open",
                        "guide": "Think about the advantages and trade-offs of each deployment strategy. Reflect on how these approaches can be tailored to meet your organization’s requirements for scalability, control, and cost-efficiency. "
                    },
                    {
                        "text": "What lessons can your organization learn from case studies of cloud adoption in leading enterprises?",
                        "type": "open",
                        "guide": "Reflect on examples of successful cloud implementations and how they addressed specific challenges or achieved strategic goals. Consider how these insights can guide your organization's cloud adoption journey. "
                    }            
                ]
            },
            unit5: {
                name: "Advanced Assessment",
                title: "Agile and DevOps ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do the principles and values of Agile methodologies align with the strategic objectives of your organization? ",
                        "type": "open",
                        "guide": "Think about how Agile promotes flexibility, collaboration, and responsiveness to change. Reflect on how these principles can enhance innovation and efficiency within your organization"
                    },
                    {
                        "text": "Which Agile tools and techniques are most applicable to your organization, and how can they support effective project management? ",
                        "type": "open",
                        "guide": "Identify specific tools, such as Kanban boards or Scrum sprints, and techniques like iterative development. Reflect on how these practices can improve team productivity, communication, and project outcomes. "
                    },
                    {
                        "text": "What challenges might your organization face when adopting DevOps practices, and how can these be mitigated? ",
                        "type": "open",
                        "guide": "Consider obstacles like cultural resistance, integration issues, or the need for new skill sets. Reflect on strategies to foster collaboration, streamline processes, and ensure the successful adoption of DevOps principles"
                    },
                    {
                        "text": "How can CI/CD and DevOps automation enhance operational efficiency in your organization?  ",
                        "type": "open",
                        "guide": "Reflect on how continuous integration, deployment, and automation can reduce errors, accelerate delivery, and improve scalability. Consider how these practices align with your organization’s goals for innovation and cost-efficiency. "
                    },
                    {
                        "text": "What lessons can your organization draw from case studies of Agile and DevOps implementation in leading tech companies?",
                        "type": "open",
                        "guide": "Reflect on examples of successful Agile and DevOps initiatives, focusing on how challenges were addressed and goals were achieved. Consider how these insights can guide your organization's adoption of these practices for long-term success. "
                    }           
                ]
            },
            unit6: {
                name: "Advanced Assessment",
                title: "Data Management and Analytics",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How can data management best practices align with the strategic objectives of your organization? ",
                        "type": "open",
                        "guide": "Think about how Agile promotes flexibility, collaboration, and responsiveness to change. Reflect on how these principles can enhance innovation and efficiency within your organization"
                    },
                    {
                        "text": "Which data analytics tools and techniques are most applicable to your organization, and how can they enhance decision-making? ",
                        "type": "open",
                        "guide": "Identify specific tools, such as Tableau or Python, and techniques like predictive analytics and visualization. Reflect on how these tools and techniques can provide actionable insights, improve forecasts, and enable data-driven decision-making processes.  "
                    },
                    {
                        "text": "What challenges might your organization face in ensuring compliance with data governance regulations, and how can these be mitigated? ",
                        "type": "open",
                        "guide": "Consider obstacles such as regulatory complexity, inconsistent data policies, or lack of stakeholder alignment. Reflect on strategies to implement governance frameworks, ensure data integrity, and address compliance gaps in your organization. "
                    },
                    {
                        "text": "How can real-world examples of data-driven decision-making inspire strategies for your organization?  ",
                        "type": "open",
                        "guide": "Reflect on case studies of successful data utilization, such as Walmart’s supply chain optimization or Netflix’s personalization strategies. Consider how these examples can guide your organization in leveraging data for innovation and competitive advantage.  "
                    },
                    {
                        "text": "What lessons can your organization draw from adopting advanced analytics techniques to achieve strategic goals? ",
                        "type": "open",
                        "guide": "Reflect on how advanced analytics, such as machine learning or big data processing, can address organizational challenges like market forecasting or customer retention. Consider how these techniques align with your organization’s objectives for growth and efficiency.  "
                    }         
                ]
            },
            unit7: {
                name: "Advanced Assessment",
                title: " Artificial Intelligence",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How can AI technologies such as machine learning, NLP, and computer vision align with your organization’s strategic goals? ",
                        "type": "open",
                        "guide": "Reflect on how these technologies support innovation, enhance customer experiences, and improve operational efficiency. Consider specific examples of how AI could streamline processes or enable new business opportunities within your organization. "
                    },
                    {
                        "text": "Which AI use cases are most relevant to your industry, and how can they drive competitive advantage? ",
                        "type": "open",
                        "guide": "dentify specific applications of AI, such as predictive maintenance in manufacturing or customer personalization in retail. Reflect on how these use cases could help your organization achieve its goals for efficiency, scalability, or market differentiation.  "
                    },
                    {
                        "text": "What challenges might your organization face when implementing AI solutions, and how can these be addressed? ",
                        "type": "open",
                        "guide": "Consider obstacles such as data quality issues, integration challenges, or workforce readiness. Reflect on strategies for overcoming these barriers, such as training programs, robust data governance, or partnerships with technology providers"
                    },
                    {
                        "text": "How can ethical considerations in AI deployment shape your organization’s strategies?  ",
                        "type": "open",
                        "guide": "Reflect on issues like data privacy, algorithmic bias, and accountability. Consider how these factors influence public trust and compliance, and how your organization can ensure responsible AI use while maintaining transparency "
                    },
                    {
                        "text": "What lessons can your organization draw from real-world examples of AI adoption in Fortune 500 companies? ",
                        "type": "open",
                        "guide": "Reflect on case studies like Netflix’s recommendation algorithms or Tesla’s autonomous driving technology. Consider how these examples highlight best practices, innovative approaches, and potential pitfalls in implementing AI solutions to drive strategic growth"
                    }          
                ]
            },
            unit8: {
                name: "Advanced Assessment",
                title: "  End-User Computing ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do key EUC technologies, such as VDI and DaaS, align with your organization’s broader goals? ",
                        "type": "open",
                        "guide": "Consider how virtual desktop infrastructure or cloud-hosted desktops might reduce hardware costs, centralize management, or improve scalability. Reflect on specific ways these technologies could support strategic initiatives, such as remote work expansion or faster provisioning of user environments."
                    },
                    {
                        "text": "Which efficiency strategies—like standardized configurations or automated software deployment—could best benefit your organization, and why? ",
                        "type": "open",
                        "guide": "Think about current bottlenecks or frequent support issues. Identify how streamlining device setups, reducing manual installations, or adopting self-service portals could address these pain points. Consider the potential impact on help desk workload, user satisfaction, and operational costs. "
                    },
                    {
                        "text": "What challenges might arise when implementing advanced support functions and automation in your EUC environment, and how can you address them? ",
                        "type": "open",
                        "guide": "Examine potential obstacles such as user resistance to new self-service tools, security concerns with remote troubleshooting, or the cost of automation software. Reflect on strategies like user training, phased rollouts, or stakeholder engagement to smooth the transition and ensure successful adoption. "
                    },
                    {
                        "text": "How can sustainability measures in EUC—like energy-efficient hardware and responsible disposal—support both environmental responsibility and cost savings?  ",
                        "type": "open",
                        "guide": "Consider the environmental impact of end-user devices throughout their lifecycle and how adopting greener initiatives (e.g., energy certifications, e-waste recycling) might align with organizational goals. Reflect on the financial benefits of lower power consumption, extended device lifespans, and reduced operational costs. "
                    },
                    {
                        "text": "What lessons can your organization draw from real-world examples of EUC optimization and automation? ",
                        "type": "open",
                        "guide": "Think of industries or enterprises that have successfully implemented centralization of services, thin clients, or help desk automation. Reflect on how these examples highlight best practices, processes for stakeholder buy-in, and measurable benefits, such as reduced downtime or streamlined support, to guide your own EUC enhancements. "
                    }         
                ]
            }
        },
    },  
    module5: {
        name: "Advanced Assessment",
        description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: "Project and Time Tracking ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do project management tools and techniques enhance collaboration and efficiency within teams? ",
                        "type": "open",
                        "guide": "Consider the features of tools like Asana, Jira, or Trello that support communication and task allocation. Reflect on how these tools can streamline workflows and ensure alignment with project goals.  "
                    },
                    {
                        "text": "What benefits does consistent time tracking bring to resource management and decision-making in your organization?",
                        "type": "open",
                        "guide": "Think about how time tracking provides data for analyzing productivity, identifying bottlenecks, and improving resource allocation. Reflect on how this supports better planning and forecasting. "
                    },
                    {
                        "text": "What challenges might teams face when implementing time tracking tools, and how can these be overcome? ",
                        "type": "open",
                        "guide": "Reflect on common barriers such as resistance to change or inconsistent usage. Consider strategies like clear communication, training, and integrating user-friendly tools to address these challenges. "
                    },
                    {
                        "text": "How does effective monitoring and reporting contribute to project transparency and stakeholder confidence? ",
                        "type": "open",
                        "guide": "think about how tools like dashboards and Gantt charts provide real-time updates and insights. Reflect on how clear reporting fosters trust and keeps projects aligned with stakeholder expectations. "
                    },
                    {
                        "text": "What lessons can be learned from case studies of organizations that successfully implemented project and time tracking strategies? ",
                        "type": "open",
                        "guide": "Reflect on examples like Agile adoption at TechInnovate or time tracking improvements at BrightFlow Consulting. Consider how these organizations overcame challenges and achieved project success.  "
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: "Contractors – Benefits and Balance ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the key advantages of hiring contractors for specific projects in your organization? ",
                        "type": "open",
                        "guide": "Consider how contractors provide access to specialized skills, flexibility for short-term needs, and cost-efficient workforce scaling. Reflect on how these benefits align with your organization’s goals."
                    },
                    {
                        "text": "What challenges might arise when integrating contractors into a team, and how can they be addressed? ",
                        "type": "open",
                        "guide": "Reflect on potential barriers such as cultural alignment, communication gaps, or knowledge transfer issues. Think about strategies like onboarding, collaborative tools, and regular feedback to mitigate these challenges. "
                    },
                    {
                        "text": "How can your organization balance the use of contractors and full-time employees to optimize workforce efficiency?",
                        "type": "open",
                        "guide": "think about the roles that contractors and full-time employees play in achieving both short-term and long-term objectives. Reflect on how this balance can enhance flexibility while maintaining stability. ."
                    },
                    {
                        "text": "What lessons can be learned from real-world examples of contractor use in tech, and how can they be applied to your organization? ",
                        "type": "open",
                        "guide": "Reflect on cases such as scaling development teams, accessing AI expertise, or managing seasonal demand. Consider how these examples illustrate the strategic use of contractors and how similar approaches could benefit your organization. ."
                    },
                    {
                        "text": "How can your organization ensure knowledge transfer and continuity when contractors complete their assignments? ",
                        "type": "open",
                        "guide": "Think about strategies like thorough documentation, collaborative workflows, and mentorship between contractors and full-time employees. Reflect on how these practices can mitigate the risk of knowledge loss and ensure long-term project success. "
                    }                             
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: "Expense Management",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do budgeting techniques enable your organization to allocate resources effectively for technology projects? ",
                        "type": "open",
                        "guide": "Consider the role of techniques like bottom-up budgeting and activity-based costing in improving accuracy and prioritizing critical investments. Reflect on how these methods can enhance project planning and execution. "
                    },
                    {
                        "text": "What challenges might arise when implementing expense tracking tools, and how can they be addressed?",
                        "type": "open",
                        "guide": "Reflect on potential obstacles such as inconsistent usage, integration issues, or resistance to change. Think about strategies like training, clear guidelines, and selecting user-friendly tools to encourage adoption and ensure accurate tracking. "
                    },
                    {
                        "text": "How can cost control strategies help your organization address budget variances and financial risks in technology projects? ",
                        "type": "open",
                        "guide": "Think about techniques such as cost-benefit analysis, vendor negotiations, and process optimization. Reflect on how these strategies can mitigate risks and ensure projects remain within budget. "
                    },
                    {
                        "text": "What lessons can your organization learn from real-world examples of successful expense management in technology projects? ",
                        "type": "open",
                        "guide": "Reflect on case studies like improving financial visibility through automated tools or achieving cost savings via vendor negotiations. Consider how these insights can be applied to optimize your organization’s expense management practices"
                    },
                    {
                        "text": "How can expense management practices align with broader organizational goals to support long-term success?",
                        "type": "open",
                        "guide": "Think about how budgeting, tracking, and reporting contribute to strategic objectives such as sustainability, innovation, and operational excellence. Reflect on how expense management integrates into the overall decision-making process in your organization"
                    }          
                ]
            },
            unit4: {
                name: "Advanced Assessment",
                title: "Unplanned Work ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How can identifying and categorizing unplanned work improve team efficiency and project outcomes? ",
                        "type": "open",
                        "guide": "Consider how categorizing unplanned work into priority levels or task types can streamline workflows and ensure that critical issues are addressed promptly. "
                    },
                    {
                        "text": "What strategies can your organization adopt to manage unplanned work without disrupting planned tasks? ",
                        "type": "open",
                        "guide": "Reflect on the importance of prioritization, buffer time, and stakeholder communication. Think about how these strategies can be tailored to your organization’s needs."
                    },
                    {
                        "text": "Which tools for tracking and reporting unplanned work would be most effective in your organization, and why? ",
                        "type": "open",
                        "guide": "Reflect on the specific needs of your team or projects. Consider how tools like Asana, Tableau, or PagerDuty could improve visibility and response times for unplanned work. "
                    },
                    {
                        "text": "What lessons from real-world examples of managing unplanned work can be applied to your organization? ",
                        "type": "open",
                        "guide": "Reflect on cases such as managing scope creep at CodeCrafters or handling seasonal demand at RetailSphere. Consider how these approaches could be adapted to your unique challenges. "
                    },
                    {
                        "text": "How can organizations balance the need to address unplanned work with the importance of achieving long-term strategic goals? ",
                        "type": "open",
                        "guide": "Think about the trade-offs between addressing immediate issues and maintaining focus on planned objectives. Reflect on how aligning tools, processes, and team collaboration can help achieve this balance. "
                    }          
                ]
            },
            unit5: {
                name: "Advanced Assessment",
                title: "FinOps ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How do the core principles of FinOps contribute to better cloud cost management and organizational collaboration? ",
                        "type": "open",
                        "guide": "Consider how cross-functional collaboration, financial accountability, and data-driven decision-making enable teams to maximize the value of cloud investments. "
                    },
                    {
                        "text": "What tools or practices would be most effective for tracking and managing cloud costs in your organization?  ",
                        "type": "open",
                        "guide": "Reflect on the specific challenges your organization faces. How could tools like AWS Cost Explorer, Microsoft Azure Cost Management, or custom dashboards improve visibility and decision-making? "
                    },
                    {
                        "text": "What strategies can your organization implement to optimize cloud spend without sacrificing performance or innovation?  ",
                        "type": "open",
                        "guide": "Reflect on approaches such as rightsizing resources, implementing auto-scaling, or leveraging reserved instances. How could these strategies align with your organization's priorities?  "
                    },
                    {
                        "text": "What lessons can be learned from the case studies on FinOps implementation, and how can they be applied to your organization’s cloud strategy? ",
                        "type": "open",
                        "guide": "Reflect on examples such as improving cost allocation at TechGlobal or leveraging automation at CloudOptix. How can these strategies be tailored to your organization’s unique needs? "
                    },
                    {
                        "text": "How can your organization foster a culture of accountability for cloud costs across technical and financial teams? ",
                        "type": "open",
                        "guide": "Consider how processes such as regular cost reviews, shared ownership of cloud budgets, and training on FinOps practices can support a collaborative approach to cost management. "
                    }
                                
                ]
            },
            unit6: {
                name: "Advanced Assessment",
                title: "Measuring Compute, Volume, and Usage  ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the most important metrics for measuring compute, volume, and usage, and why are they critical for cloud resource management? ",
                        "type": "open",
                        "guide": "Consider metrics such as CPU utilization, storage capacity, and bandwidth. Reflect on how these metrics help identify inefficiencies and inform decision-making. "
                    },
                    {
                        "text": "Which tools for monitoring and reporting resource usage would be most beneficial for your organization, and why?  ",
                        "type": "open",
                        "guide": "Reflect on tools like AWS CloudWatch, Azure Monitor, or open-source alternatives. How could these tools improve your organization’s ability to track and optimize cloud resources?  "
                    },
                    {
                        "text": "What strategies can your organization implement to optimize resource usage while maintaining performance and cost-efficiency?  ",
                        "type": "open",
                        "guide": "Think about techniques such as right-sizing, lifecycle management, and leveraging spot instances. Reflect on how these strategies align with your organization’s goals. "
                    },
                    {
                        "text": "What lessons can be learned from the case studies on resource management, and how can they be applied to your organization’s cloud strategy? ",
                        "type": "open",
                        "guide": "Reflect on examples such as automating lifecycle policies at a financial services firm or adopting predictive analytics at a global retailer. How can these practices address challenges in your organization? "
                    },
                    {
                        "text": "How can your organization balance the need to address unplanned resource spikes with the goal of maintaining long-term cost control?  ",
                        "type": "open",
                        "guide": "Consider strategies such as proactive monitoring, dynamic scaling, and stakeholder collaboration. Reflect on how aligning operational processes with strategic goals can help achieve this balance."
                    }           
                ]
            }
        }
    },
    module6: {
        name: "Advanced Assessment",
        description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: "Benchmarking – Staying Competitive ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the key benefits of using benchmarking to assess organizational performance?  ",
                        "type": "open",
                        "guide": "Reflect on how benchmarking enables organizations to identify performance gaps, adopt best practices, and improve competitiveness. Consider specific examples from your own organization or industry"
                    },
                    {
                        "text": "How can organizations select KPIs that align with their strategic goals?",
                        "type": "open",
                        "guide": "Think about the importance of aligning KPIs with broader business objectives. Reflect on how to ensure that chosen KPIs are measurable, relevant, and actionable. "
                    },
                    {
                        "text": "What tools or techniques for benchmarking would be most effective in your organization, and why?",
                        "type": "open",
                        "guide": "Consider how tools like Tableau, MetricNet, or benchmarking dashboards could be used to monitor, analyze, and report performance metrics in your organization."
                    },
                    {
                        "text": "What are the most common challenges faced during benchmarking, and how can they be addressed? ",
                        "type": "open",
                        "guide": "Reflect on challenges such as data availability, resource constraints, and resistance to change. How can fostering a culture of continuous improvement help overcome these barriers? "
                    },
                    {
                        "text": "What lessons from real-world case studies on benchmarking can be applied to your organization?  ",
                        "type": "open",
                        "guide": "Think about case studies covered in this unit. How can their approaches to adopting KPIs, overcoming challenges, or leveraging tools inform your organization’s benchmarking strategy? "
                    },
                    {
                        "text": "How can benchmarking be integrated into an organization’s ongoing performance management processes? ",
                        "type": "open",
                        "guide": "Reflect on the role of benchmarking in driving continuous improvement. How can organizations ensure that benchmarking is a regular and actionable part of their strategic planning? "
                    },
                    {
                        "text": "How can organizations ensure team buy-in and collaboration during benchmarking initiatives? ",
                        "type": "open",
                        "guide": "Consider the role of communication, stakeholder engagement, and fostering a learning culture. How can these practices support successful benchmarking efforts?"
                    },
                    {
                        "text": "How does benchmarking contribute to an organization’s ability to stay competitive in a dynamic market? ",
                        "type": "open",
                        "guide": "Reflect on how benchmarking enables organizations to adapt to industry changes, improve efficiency, and enhance customer satisfaction. "
                    },
                    {
                        "text": "What are the potential risks of relying too heavily on benchmarking, and how can they be mitigated?  ",
                        "type": "open",
                        "guide": "Consider risks such as over-focusing on competitor comparisons or using outdated benchmarks. How can organizations maintain a balanced approach? "
                    },
                    {
                        "text": "What steps can your organization take to move from benchmarking insights to actionable improvements? ",
                        "type": "open",
                        "guide": "Reflect on how to translate benchmarking findings into tangible actions. Consider strategies like prioritizing improvements, setting clear goals, and involving cross-functional teams. "
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: "Technology Management Analytics ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the critical features of technology management analytics tools, and how do they contribute to organizational performance? ",
                        "type": "open",
                        "guide": "Reflect on how these tools provide actionable insights, automate data collection, and improve decision-making processes. Consider specific tools or platforms relevant to your organization"
                    },
                    {
                        "text": "How can data-driven decision-making improve operational efficiency and strategic alignment in your organization?  ",
                        "type": "open",
                        "guide": "Think about the role of analytics in aligning decisions with business goals. How does using accurate and relevant data enhance decision quality? "
                    },
                    {
                        "text": "What performance measurement techniques would be most beneficial for your organization, and why? ",
                        "type": "open",
                        "guide": "Reflect on metrics such as cycle time, MTTR, or employee productivity. How can these measurements inform improvements and optimize operations? ."
                    },
                    {
                        "text": "How can organizations ensure that analytics insights are translated into actionable improvements? ",
                        "type": "open",
                        "guide": "Consider the importance of setting clear objectives, involving cross-functional teams, and prioritizing improvements based on analytics findings."
                    },
                    {
                        "text": "What lessons can your organization draw from real-world examples of technology management analytics? ",
                        "type": "open",
                        "guide": "Reflect on case studies covered in this unit. How can their strategies for deploying analytics tools or overcoming challenges be adapted to your context?"
                    },
                    {
                        "text": "What are the most common challenges organizations face when implementing technology management analytics, and how can they be addressed?  ",
                        "type": "open",
                        "guide": "Reflect on challenges such as data silos, resistance to change, or resource constraints. How can fostering collaboration and providing training mitigate these issues? ?"
                    },
                    {
                        "text": "How can organizations balance the use of historical data with predictive analytics to drive future success? ",
                        "type": "open",
                        "guide": "Think about the value of lagging and leading indicators. How can combining both types of data improve planning and strategy? "
                    },
                    {
                        "text": "How does analytics-driven performance measurement support continuous improvement?  ",
                        "type": "open",
                        "guide": "Reflect on how ongoing measurement enables organizations to identify inefficiencies, refine processes, and maintain competitiveness in dynamic markets. "
                    },
                    {
                        "text": "What strategies can organizations use to encourage cross-departmental collaboration in leveraging analytics tools?  ",
                        "type": "open",
                        "guide": "Consider practices such as data democratization, shared dashboards, or regular analytics reviews. How do these strategies improve alignment and collaboration?  "
                    },
                    {
                        "text": "How can your organization foster a culture of analytics adoption and accountability? ",
                        "type": "open",
                        "guide": "Reflect on the role of leadership, training, and incentives. How can these factors drive broader acceptance and effective use of analytics tools?   "
                    }                                
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: " Integrated Line-of-Business Analytics",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the key benefits of integrating business analytics with technology in an organization? ",
                        "type": "open",
                        "guide": "Consider how this integration fosters real-time decision-making, enhances collaboration, and improves operational efficiency. Reflect on examples where analytics have driven strategic advantages."
                    },
                    {
                        "text": "How can cross-functional analytics tools improve collaboration and decision-making in your organization? ",
                        "type": "open",
                        "guide": "Reflect on how tools like Tableau, Microsoft Power BI, or Looker can streamline workflows and provide a unified platform for various teams to access and analyze data effectively. "
                    },
                    {
                        "text": "What challenges might an organization face when implementing integrated analytics, and how can they be overcome?  ",
                        "type": "open",
                        "guide": "Consider challenges such as data silos, lack of technical expertise, or resistance to change. Reflect on strategies like fostering a data-driven culture and investing in training programs."
                    },
                    {
                        "text": "What are the essential characteristics of an effective analytics strategy for achieving strategic objectives? ",
                        "type": "open",
                        "guide": "Reflect on the importance of aligning analytics initiatives with organizational goals, selecting meaningful KPIs, and leveraging predictive and prescriptive insights"
                    },
                    {
                        "text": "How can organizations measure the success of integrated analytics initiatives? ",
                        "type": "open",
                        "guide": "Think about metrics such as improved decision-making speed, enhanced operational efficiency, or increased ROI. Reflect on how these measures align with broader business goals.  "
                    },
                    {
                        "text": "What lessons can be learned from the case studies of integrated analytics in tech, and how can they apply to your organization?  ",
                        "type": "open",
                        "guide": "Reflect on how companies like Netflix, Amazon, or Google leverage integrated analytics to achieve competitive advantages and consider how their practices could inspire similar strategies in your organization.   "
                    },
                    {
                        "text": "How can integrated analytics support proactive decision-making and risk management? ",
                        "type": "open",
                        "guide": "Reflect on how predictive and prescriptive analytics can help organizations identify trends, forecast outcomes, and mitigate potential risks effectively.  "
                    },
                    {
                        "text": "What role does data governance play in successful integrated analytics implementations? ",
                        "type": "open",
                        "guide": "Consider the importance of data accuracy, security, and compliance in ensuring that analytics initiatives deliver reliable and actionable insights. "
                    },
                    {
                        "text": "How can organizations ensure team buy-in and collaboration during the adoption of integrated analytics tools?  ",
                        "type": "open",
                        "guide": "Reflect on the importance of communication, leadership support, and demonstrating the tangible benefits of analytics tools to all stakeholders "
                    },
                    {
                        "text": "What steps can your organization take to move from analytics insights to actionable strategies and outcomes? ",
                        "type": "open",
                        "guide": "Reflect on how to create action plans, set measurable goals, and involve cross-functional teams in translating analytics insights into impactful business decisions."
                    }              
                ]
            },
            unit4: {
                name: "Advanced Assessment",
                title: "Top-Down vs. Bottom-Up Analysis  ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the key differences between the Top-Down and Bottom-Up approaches in organizational decision-making? ",
                        "type": "open",
                        "guide": "Reflect on how these differences impact strategic alignment, resource allocation, and innovation"
                    },
                    {
                        "text": "In what scenarios is the Top-Down approach most effective, and why?  ",
                        "type": "open",
                        "guide": "Consider scenarios such as crisis management, large-scale rollouts, or centralized planning. "
                    },
                    {
                        "text": "How can the Bottom-Up approach foster innovation and employee engagement within an organization? ",
                        "type": "open",
                        "guide": "Think about how employee-driven initiatives and decentralized decision-making create value. "
                    },
                    {
                        "text": "What are the primary challenges organizations face when implementing a Bottom-Up approach?  ",
                        "type": "open",
                        "guide": "Reflect on challenges such as aligning decentralized initiatives with broader strategic goals.  "
                    },
                    {
                        "text": "How can a hybrid approach combine the strengths of both Top-Down and Bottom-Up methods? ",
                        "type": "open",
                        "guide": "Consider examples where leadership sets the vision, but teams have autonomy in execution.  "
                    },
                    {
                        "text": "What tools or technologies can support effective implementation of the Bottom-Up approach?  ",
                        "type": "open",
                        "guide": "Think about collaboration tools, feedback platforms, or innovation hubs that empower employees.  "
                    },
                    {
                        "text": "How does a Top-Down approach ensure alignment with organizational objectives during large-scale initiatives?  ",
                        "type": "open",
                        "guide": "Reflect on the role of leadership in creating clarity and ensuring cohesive execution.   "
                    },
                    {
                        "text": "What lessons can be drawn from the case studies of technology companies using hybrid approaches? ",
                        "type": "open",
                        "guide": "Consider examples such as Amazon or Microsoft, and how they balance centralized strategy with local autonomy.  "
                    },
                    {
                        "text": "What are the risks of over-relying on either the Top-Down or Bottom-Up approach, and how can they be mitigated?",
                        "type": "open",
                        "guide": "Reflect on the trade-offs between control and flexibility, and the importance of balanced strategies.  "
                    },
                    {
                        "text": "How can organizations transition from a rigid Top-Down structure to a more flexible hybrid approach? ",
                        "type": "open",
                        "guide": "Consider steps such as fostering a culture of trust, providing training, and implementing collaborative tools  "
                    }          
                ]
            }
        }
    },
    module7: {
    name: "Advanced Assessment",
    description: "Advanced concepts in financial and strategic planning",
        units: {
            unit1: {
                name: "Advanced Assessment",
                title: " Demand Analytics  ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the core principles of demand analytics, and how do they support effective decision-making in businesses?   ",
                        "type": "open",
                        "guide": "Reflect on the importance of demand forecasting, data-driven insights, and aligning analytics with organizational goals. How do these principles improve organizational responsiveness? "
                    },
                    {
                        "text": "How can organizations select the most effective tools and techniques for demand forecasting? ",
                        "type": "open",
                        "guide": "Consider the specific challenges your organization faces. Which tools (e.g., Amazon Forecast, Tableau) would best address these challenges, and why?"
                    },
                    {
                        "text": "What is the significance of analyzing market trends in predicting future customer demand? ",
                        "type": "open",
                        "guide": "Reflect on how tracking market trends enables organizations to identify opportunities and mitigate risks. How does this influence long-term strategies? "
                    },
                    {
                        "text": "How does understanding customer behavior contribute to demand analytics?  ",
                        "type": "open",
                        "guide": "Reflect on how customer segmentation, purchase patterns, and preferences inform forecasting models. How can this knowledge drive personalized marketing strategies? "
                    },
                    {
                        "text": "What lessons can be learned from real-world case studies on demand analytics in technology companies?   ",
                        "type": "open",
                        "guide": "Consider how organizations like Amazon, Apple, or Microsoft have successfully implemented demand analytics. What best practices or strategies can you apply in your own organization?  "
                    },
                    {
                        "text": "What role does collaboration between departments (e.g., marketing, operations, finance) play in successful demand analytics initiatives?",
                        "type": "open",
                        "guide": "Reflect on obstacles such as data quality issues, technology adoption, or resistance to change. How can fostering a culture of continuous improvement address these challenges?  "
                    },
                    {
                        "text": "What challenges do organizations face in demand analytics, and how can these challenges be mitigated? ",
                        "type": "open",
                        "guide": "Consider the role of communication, stakeholder engagement, and fostering a learning culture. How can these practices support successful benchmarking efforts?"
                    },
                    {
                        "text": "How can demand analytics support sustainability and resource optimization in an organization?  ",
                        "type": "open",
                        "guide": "Reflect on how predictive modeling can reduce waste, optimize inventory, and align production with actual demand. "
                    },
                    {
                        "text": "What are the potential risks of relying too heavily on historical data in demand forecasting?  ",
                        "type": "open",
                        "guide": "Consider how changes in market dynamics, customer preferences, or global disruptions could impact forecasting accuracy. How can organizations remain adaptive? "
                    },
                    {
                        "text": "How can your organization translate demand analytics insights into actionable strategies? ",
                        "type": "open",
                        "guide": "Reflect on the steps required to implement findings, such as prioritizing improvements, setting measurable goals, and involving key stakeholders. What processes would best support this transformation? "
                    }
                ]
            },
            unit2: {
                name: "Advanced Assessment",
                title: " Tread Analysis  ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "How can trend analysis help organizations adapt to changing market dynamics?  ",
                        "type": "open",
                        "guide": "Consider specific examples of how companies have used trend analysis to remain competitive and responsive to customer needs. "
                    },
                    {
                        "text": "What tools for trend analysis would be most beneficial in your organization, and why? ",
                        "type": "open",
                        "guide": "Reflect on tools such as Tableau, Microsoft Power BI, or Google Trends and how they might align with your organization’s needs.  "
                    },
                    {
                        "text": "How does analyzing trends contribute to strategic technology investments?  ",
                        "type": "open",
                        "guide": "Think about how trend analysis can guide decisions on adopting or scaling specific technologies. "
                    },
                    {
                        "text": "What are some potential challenges in identifying trends, and how can they be mitigated? ",
                        "type": "open",
                        "guide": "Reflect on issues such as data reliability, rapid market changes, or bias in analysis. ."
                    },
                    {
                        "text": "How do real-world examples from companies like Apple or Amazon illustrate the value of trend analysis? ",
                        "type": "open",
                        "guide": "Identify key lessons from the case studies provided in this unit and how they apply to other businesses. "
                    },
                    {
                        "text": "How can trend analysis foster innovation within an organization?  ",
                        "type": "open",
                        "guide": "Reflect on challenges such as data silos, resistance to change, or resource constraints. How can fostering collaboration and providing training mitigate these issues? ?"
                    },
                    {
                        "text": "What role does collaboration play in effective trend analysis?  ",
                        "type": "open",
                        "guide": "Consider how cross-departmental insights and teamwork can enhance the accuracy and relevance of trend analysis"
                    } ,
                    {
                        "text": "How can predictive analytics enhance the trend analysis process?  ",
                        "type": "open",
                        "guide": "Reflect on the benefits of integrating AI and machine learning tools into trend analysis frameworks.  "
                    },
                    {
                        "text": "What steps can your organization take to transition from analyzing trends to actionable insights? ",
                        "type": "open",
                        "guide": "Think about how to turn findings from trend analysis into strategic initiatives or operational improvements. "
                    },
                    {
                        "text": "How does trend analysis align with the overarching goals of technology management? ",
                        "type": "open",
                        "guide": "Reflect on the role of trend analysis in supporting long-term organizational goals and maintaining competitive positioning "
                    }                                
                ]
            },
            unit3: {
                name: "Advanced Assessment",
                title: " Moore’s Law ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the core principles of Moore’s Law, and how have they influenced the evolution of technology over the past decades? ",
                        "type": "open",
                        "guide": "Reflect on the doubling of transistor density and its impact on computing power, efficiency, and technological innovation. "
                    },
                    {
                        "text": "How has Moore’s Law shaped the strategies and competitive positioning of leading technology companies like Intel and NVIDIA?  ",
                        "type": "open",
                        "guide": "Consider the role of Moore’s Law in driving advancements in semiconductors, processors, and other foundational technologies.  "
                    },
                    {
                        "text": "What challenges do companies face as Moore’s Law approaches its physical and economic limits? ",
                        "type": "open",
                        "guide": "Analyze issues like heat dissipation, power consumption, and the rising costs of maintaining transistor scaling. ."
                    },
                    {
                        "text": "How can organizations adapt to the slowing of Moore’s Law to sustain innovation and maintain competitive advantages? ",
                        "type": "open",
                        "guide": "Reflect on strategies such as leveraging parallel processing, exploring alternative architectures, and investing in quantum computing. "
                    },
                    {
                        "text": "What are the broader economic implications of Moore’s Law for industries beyond technology, such as healthcare, automotive, and finance?  ",
                        "type": "open",
                        "guide": "TConsider how advancements in computing power have transformed data analytics, AI, and other applications across industries.  "
                    },
                    {
                        "text": "How do real-world case studies of Moore’s Law in action illustrate its impact on technology adoption and market growth?   ",
                        "type": "open",
                        "guide": "Reflect on examples of how companies have applied Moore’s Law to launch innovative products and capture new markets.  "
                    },
                    {
                        "text": "What role does Moore’s Law play in shaping long-term research and development (R&D) strategies for technology companies? ",
                        "type": "open",
                        "guide": "Consider how the principles of Moore’s Law guide investments in emerging technologies and next-generation solutions"
                    },
                    {
                        "text": "How can emerging technologies like AI, machine learning, and quantum computing complement or replace traditional Moore’s Law scaling?  ",
                        "type": "open",
                        "guide": "Explore the potential of these technologies to address the limitations of transistor miniaturization and drive future innovation.  "
                    },
                    {
                        "text": "In what ways can Moore’s Law inform business leaders’ decision-making processes regarding technology adoption and infrastructure investments? ",
                        "type": "open",
                        "guide": "Reflect on how insights from Moore’s Law can support data-driven strategies and resource allocation.  "
                    },
                    {
                        "text": " What lessons can organizations learn from the historical impact of Moore’s Law to prepare for future challenges and opportunities in technology development?  ",
                        "type": "open",
                        "guide": "Analyze how an understanding of Moore’s Law can help organizations remain resilient and adaptable in a rapidly changing technological landscape"
                    }             
                ]
            },
            unit4: {
                name: "Advanced Assessment",
                title: "Automation Limits   ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What are the primary limitations of automation in complex decision-making processes?  ",
                        "type": "open",
                        "guide": "Reflect on scenarios where human oversight is essential and how automation can fail to consider ethical, contextual, or nuanced factors. "
                    },
                    {
                        "text": "How can organizations achieve a balance between automation and human oversight?  ",
                        "type": "open",
                        "guide": "Consider strategies for integrating human judgment with automated systems to ensure ethical and effective decision-making. "
                    },
                    {
                        "text": "What are some of the ethical challenges organizations face when implementing automation?  ",
                        "type": "open",
                        "guide": "Reflect on issues like potential biases in automated systems, job displacement, and the need for transparency in decision-making processes. "
                    },
                    {
                        "text": "How can companies address resistance to automation among employees?   ",
                        "type": "open",
                        "guide": "Think about strategies like workforce retraining, clear communication, and fostering a culture of collaboration to ease transitions  "
                    },
                    {
                        "text": "What are the potential risks of over-reliance on automation in critical organizational processes? ",
                        "type": "open",
                        "guide": "Reflect on examples where over-reliance on automation led to errors or inefficiencies and how organizations can mitigate these risks.  "
                    },
                    {
                        "text": "How does the integration of AI and machine learning enhance the capabilities of automation?  ",
                        "type": "open",
                        "guide": "Explore how predictive and prescriptive analytics can improve decision-making and operational efficiency when combined with automation.  "
                    },
                    {
                        "text": "What practical steps can organizations take to ensure the ethical deployment of automation?  ",
                        "type": "open",
                        "guide": "Reflect on the role of ethical guidelines, stakeholder involvement, and transparent practices in automation implementation.    "
                    },
                    {
                        "text": "How can automation contribute to operational efficiency while maintaining a human-centric approach?  ",
                        "type": "open",
                        "guide": "Consider how automation can streamline repetitive tasks while enabling employees to focus on strategic and creative activities. "
                    },
                    {
                        "text": "What role does training and development play in supporting employees during automation transitions?",
                        "type": "open",
                        "guide": "Reflect on the importance of equipping employees with the skills to adapt to and work alongside automation technologies  "
                    },
                    {
                        "text": "How can real-world examples of automation implementation in Fortune 500 companies guide your organization’s strategy?  ",
                        "type": "open",
                        "guide": "Analyze case studies from leading companies to identify best practices, challenges, and lessons learned in automation deployment.  "
                    }       
                ]
            },
            unit5: {
                name: "Advanced Assessment",
                title: "Technology Intensity    ",
                description: "Test your advanced understanding of the concepts.",
                questions: [
                    {
                        "text": "What is the significance of technology intensity in modern organizations?   ",
                        "type": "open",
                        "guide": "Reflect on how technology intensity influences innovation, resource allocation, and strategic decision-making within organizations. Consider specific examples from your own industry. "
                    },
                    {
                        "text": "How can organizations accurately measure their technology intensity?  ",
                        "type": "open",
                        "guide": "Think about the tools and metrics discussed in this unit, such as R&D investment percentages and technology readiness levels. Reflect on how these metrics align with business objectives.. "
                    },
                    {
                        "text": "What challenges do organizations face in managing and optimizing technology intensity?  ",
                        "type": "open",
                        "guide": "Consider barriers such as high R&D costs, integration challenges, and resistance to change. Reflect on strategies for overcoming these obstacles.  "
                    },
                    {
                        "text": "How does technology intensity contribute to maintaining a competitive edge? ",
                        "type": "open",
                        "guide": "Reflect on how organizations like Tesla, Amazon, and Apple leverage technology intensity to innovate and remain market leaders.  "
                    },
                    {
                        "text": "What role do cross-functional teams play in optimizing technology intensity?  ",
                        "type": "open",
                        "guide": "Think about the importance of collaboration between departments, such as IT, R&D, and operations, to maximize the value of technological investments.   "
                    },
                    {
                        "text": "What are the risks of focusing too much or too little on technology intensity?   ",
                        "type": "open",
                        "guide": "Reflect on the potential downsides, such as over-reliance on technology or lagging behind competitors. How can organizations balance these risks? "
                    },
                    {
                        "text": "How can technology intensity drive sustainability and long-term growth?  ",
                        "type": "open",
                        "guide": "Consider the role of scalable technologies and forward-thinking strategies in achieving sustainable business models.    "
                    },
                    {
                        "text": "How do global trends influence technology intensity strategies? ",
                        "type": "open",
                        "guide": "Reflect on the impact of emerging technologies like AI and quantum computing and how they shape organizational approaches to technology intensity"
                    },
                    {
                        "text": "What lessons from the case studies can be applied to your organization? ",
                        "type": "open",
                        "guide": "Think about how leading companies addressed challenges and leveraged technology intensity to drive success. How can these insights be adapted to your context?  "
                    },
                    {
                        "text": "What steps can organizations take to embed technology intensity into their strategic planning processes?  ",
                        "type": "open",
                        "guide": "Reflect on best practices such as aligning R&D efforts with business goals, fostering a culture of innovation, and investing in emerging technologies.   "
                    }          
                ]
            }                        
        }
    }
}

// Get module and unit from the page URL
function getModuleAndUnit() {
    // First try to get module and unit from query parameters
    const queryParams = new URLSearchParams(window.location.search);
    const moduleParam = queryParams.get('module');
    const unitParam = queryParams.get('unit');
    
    if (moduleParam && unitParam) {
        return {
            moduleId: `module${moduleParam}`,
            unitId: `unit${unitParam}`
        };
    }
    
    // Fallback to filename parsing if no query params
    const path = window.location.pathname;
    const filename = path.split('/').pop();
    const match = filename.match(/^(module\d+)_(unit\d+)\.html$/);
    
    if (match) {
        return {
            moduleId: match[1],
            unitId: match[2]
        };
    }
    
    // Default values if no method works
    return {
        moduleId: 'module1',
        unitId: 'unit1'
    };
}

function getConfig() {
    const { moduleId, unitId } = getModuleAndUnit();
    const module = moduleConfig[moduleId];
    const unit = module?.units[unitId];
    
    if (!module || !unit) {
        console.error(`Configuration not found for ${moduleId}/${unitId}`);
        return {
            moduleId: 'module1',
            unitId: 'unit1',
            module: moduleConfig.module1,
            unit: moduleConfig.module1.units.unit1
        };
    }
    
    return {
        moduleId,
        unitId,
        module,
        unit
    };
}

// Export configurations
window.moduleConfig = moduleConfig;
window.getConfig = getConfig;
window.API_BASE_URL = API_BASE_URL;
window.API_TIMEOUT = API_TIMEOUT; 