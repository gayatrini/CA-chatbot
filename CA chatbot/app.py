from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

# Define the pairs for the chatbot
# Pairs is a list of patterns and responses tailored for accounting-related questions from customers.
# Define the pairs for the chatbot
pairs = [

    # Greetings and conversation starters
    [
        r"hi|hello",
        ["Hello! I'm your virtual CA. How can I assist you today?",]
    ],
    [
        r"(.*) your name ?",
        ["My name is CA Bot. How can I assist you with your accounting needs today?",]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you for asking! how are you doing?",]
    ],
     [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind that",]
    ],
    [
        r"i'm (good|well|okay|ok)",
        ["Nice to hear that","Alright, great !",]
    ],
    [
        r"i am (good|well|okay|ok)",
        ["Nice to hear that","Alright, great !",]
    ],
    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello", "Hey there",]
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
        
    ],
    [
        r"what can you do ?",
        ["I can assist you with financial accounting, taxation, financial advice, and more. Just ask me!",]
    ],
    [
        r"bye|goodbye",
        ["Goodbye! If you have any more questions, feel free to ask.",]
    ],
    
    # Basic accounting concepts
    [
        r"(.*) double-entry accounting",
        ["Double-entry accounting means that every financial transaction has equal and opposite effects on at least two accounts.",]
    ],
    [
        r"(.*) balance sheet",
        ["A balance sheet lists a company's assets, liabilities, and equity as of a specific date.",]
    ],
    [
        r"(.*) income statement",
        ["An income statement shows a company's revenues and expenses over a specific period, resulting in net income or loss.",]
    ],
    
    # Taxation support
    [
        r"(.*) file tax returns",
        ["To file tax returns, gather all necessary documents and information and submit them to the relevant tax authority.",]
    ],
    [
        r"(.*) tax planning",
        ["Tax planning involves optimizing your financial situation to minimize your tax liability legally.",]
    ],
    
    # Financial advice
    [
        r"(.*) investment strategies",
        ["Investment strategies depend on your financial goals, risk tolerance, and investment horizon. I can provide guidance based on your preferences.",]
    ],
    [
        r"(.*) budgeting tips",
        ["Budgeting involves creating a plan for your income and expenses. I can help you with tips to manage your budget effectively.",]
    ],
    
    # Audit and compliance
    [
        r"(.*) audit process",
        ["The audit process involves reviewing financial statements to ensure accuracy and compliance with accounting standards.",]
    ],
    [
        r"(.*) compliance with regulations",
        ["It's important to comply with regulations such as the Income Tax Act, GST Act, and Companies Act to avoid penalties and legal issues.",]
    ],
    
    # Financial reporting
    [
        r"(.*) financial reporting",
        ["Financial reporting involves preparing and presenting financial statements and reports to stakeholders.",]
    ],
    [
        r"(.*) internal reporting",
        ["Internal reporting provides management with financial information to support decision-making.",]
    ],
    
    # Accounting services
    [
        r"(.*) accounting services",
        ["Our accounting services include bookkeeping, financial statement preparation, payroll processing, and management accounting.",]
    ],
    [
        r"(.*) consultancy services",
        ["We offer consultancy services for SMEs, including business planning, financial analysis, and strategic advice.",]
    ],
    
    # Miscellaneous
    [
        r"(.*) financial ratios",
        ["Financial ratios are metrics used to evaluate a company's financial performance, such as profitability ratios, liquidity ratios, and solvency ratios.",]
    ],
    [
        r"(.*) importance of insurance",
        ["Insurance provides protection against financial losses due to unexpected events. It's important to have adequate insurance coverage.",]
    ],
    [
        r"(.*) insurance is important(.*)",
        ["Insurance provides protection against financial losses due to unexpected events. It's important to have adequate insurance coverage.",]
    ],


    # Debt and equity financing
    [
        r"(.*) debt financing",
        ["Debt financing involves raising capital by borrowing money, typically through loans or bonds, which must be repaid with interest.",]
    ],
    [
        r"(.*) equity financing",
        ["Equity financing involves raising capital by selling shares of ownership in the company, giving investors a stake in the business in exchange for funding.",]
    ],
    [
        r"(.*) cost of capital",
        ["The cost of capital is the rate of return that a company must earn on its investments to maintain or increase its value.",]
    ],
    [
        r"(.*) time value of money",
        ["The time value of money refers to the principle that a dollar today is worth more than a dollar in the future due to its potential earning capacity.",]
    ],
    [
        r"(.*) investment opportunities",
        ["Investment opportunities refer to the various options available for individuals or businesses to invest their money, such as stocks, bonds, real estate, or mutual funds.",]
    ],
    
    # Financial markets and risk analysis
    [
        r"(.*) financial risk analysis",
        ["Financial risk analysis involves identifying and assessing the potential risks that could impact an organization's financial performance or objectives.",]
    ],
    [
        r"(.*) financial markets",
        ["Financial markets are platforms where individuals and institutions trade financial securities, commodities, and other fungible items at prices determined by supply and demand.",]
    ],
    [
        r"(.*) stock",
        ["A stock represents ownership in a corporation and entitles the owner to a share of the company's assets and profits.",]
    ],
    [
        r"(.*) bond",
        ["A bond is a fixed-income investment in which an investor loans money to an entity (typically a corporation or government) that borrows the funds for a defined period at a fixed interest rate.",]
    ],
    [
        r"(.*) credit ratings",
        ["Credit ratings are assessments of the creditworthiness of individuals, businesses, or securities based on their ability to repay debt obligations.",]
    ],
    
    # Corporate finance and valuation
    [
        r"(.*) company valuation",
        ["Company valuation is the process of determining the economic value of a business or its assets, typically for investment, acquisition, or financial reporting purposes.",]
    ],
    [
        r"(.*) capital budgeting",
        ["Capital budgeting is the process of evaluating and selecting long-term investment projects or expenditures that will generate future cash flows for a company.",]
    ],
    [
        r"(.*) financial modeling",
        ["Financial modeling is the process of creating a mathematical representation of a financial situation or business decision to analyze the impact of different variables and scenarios.",]
    ],
    [
        r"(.*) leveraged buyout",
        ["A leveraged buyout (LBO) is a financial transaction in which a company is acquired using a significant amount of borrowed money to meet the cost of acquisition.",]
    ],
    [
        r"(.*) financial derivatives",
        ["Financial derivatives are contracts whose value is derived from the performance of an underlying asset, index, or rate, such as options, futures, and swaps.",]
    ],
    
    # Forensic audit and fraud prevention
    [
        r"(.*) forensic audit",
        ["A forensic audit is an examination of financial records and transactions to uncover fraud, embezzlement, or other illegal activities.",]
    ],
    [
        r"(.*) insurance fraud",
        ["Insurance fraud involves deliberately deceiving an insurance company for financial gain, such as by filing false claims or providing misleading information.",]
    ],
    [
        r"(.*) anti-fraud measures",
        ["Anti-fraud measures are policies, procedures, and controls implemented by organizations to detect, prevent, and deter fraudulent activities.",]
    ],
    [
        r"(.*) whistleblower protection",
        ["Whistleblower protection laws are designed to protect individuals who report illegal or unethical behavior within an organization from retaliation or harassment.",]
    ],
    [
        r"(.*) fraud detection techniques",
        ["Fraud detection techniques include data analysis, forensic accounting, internal controls, and employee training to identify suspicious behavior or transactions.",]
    ],
    
    # Insurance-related queries
    [
        r"(.*) types of insurance",
        ["There are various types of insurance, including life insurance, health insurance, property insurance, liability insurance, and automobile insurance.",]
    ],
    [
        r"(.*) insurance premium",
        ["An insurance premium is the amount of money an individual or business pays to an insurance company in exchange for insurance coverage.",]
    ],
    [
        r"(.*) insurance claim",
        ["An insurance claim is a formal request made by a policyholder to an insurance company for compensation or coverage for a covered loss or event.",]
    ],
    [
        r"(.*) insurance policy",
        ["An insurance policy is a contract between an insurance company and a policyholder that outlines the terms and conditions of insurance coverage.",]
    ],
    [
        r"(.*) insurance coverage limits",
        ["Insurance coverage limits are the maximum amounts an insurance policy will pay for covered losses or events, as specified in the policy terms.",]
    ],
    
    # Financial planning and investment queries
    [
        r"(.*) retirement planning",
        ["Retirement planning involves setting financial goals and creating a savings and investment strategy to ensure a comfortable retirement.",]
    ],
    [
        r"(.*) investment portfolio diversification",
        ["Investment portfolio diversification is the practice of spreading investments across different asset classes, sectors, and geographic regions to reduce risk and maximize returns.",]
    ],
    [
        r"(.*) risk tolerance assessment",
        ["Risk tolerance assessment helps individuals and investors understand their willingness and ability to accept investment risk in pursuit of their financial goals.",]
    ],
    [
        r"(.*) financial goal setting",
        ["Financial goal setting involves identifying short-term and long-term objectives, such as saving for retirement, buying a home, or funding education, and creating a plan to achieve them.",]
    ],
    [
        r"(.*) tax-efficient investment strategies",
        ["Tax-efficient investment strategies aim to minimize taxes on investment income and capital gains through strategies such as tax-deferred accounts, tax-loss harvesting, and asset location optimization.",]
    ],
    
    # Accounting principles and standards
    [
        r"(.*) accounting principles",
        ["Accounting principles are the rules and guidelines that govern the preparation and presentation of financial statements, such as the accrual basis of accounting, revenue recognition principle, and matching principle.",]
    ],
    [
        r"(.*) international accounting standards",
        ["International accounting standards are a set of guidelines and rules issued by the International Accounting Standards Board (IASB) to ensure consistency and comparability in financial reporting across countries and industries.",]
    ],
    [
        r"(.*) compliance with accounting standards",
        ["Compliance with accounting standards requires companies to adhere to the principles and rules set forth by regulatory bodies such as the Financial Accounting Standards Board (FASB) or the International Financial Reporting Standards (IFRS) Foundation.",]
    ],
    [
        r"(.*) audit trail",
        ["An audit trail is a systematic record of the transactions and events that have occurred within an accounting system, providing a chronological history of financial activities and changes.",]
    ],
    [
        r"(.*) financial statement analysis",
        ["Financial statement analysis involves reviewing and interpreting a company's financial statements to assess its financial performance, liquidity, solvency, and profitability.",]
    ],

    # Debt and equity financing
    [
        r"(.*) debt financing",
        ["Debt financing involves raising capital by borrowing money, typically through loans or bonds, which must be repaid with interest.",]
    ],
    [
        r"(.*) equity financing",
        ["Equity financing involves raising capital by selling shares of ownership in the company, giving investors a stake in the business in exchange for funding.",]
    ],
    [
        r"(.*) cost of capital",
        ["The cost of capital is the rate of return that a company must earn on its investments to maintain or increase its value.",]
    ],
    [
        r"(.*) time value of money",
        ["The time value of money refers to the principle that a dollar today is worth more than a dollar in the future due to its potential earning capacity.",]
    ],
    [
        r"(.*) investment opportunities",
        ["Investment opportunities refer to the various options available for individuals or businesses to invest their money, such as stocks, bonds, real estate, or mutual funds.",]
    ],
    
    # Financial markets and risk analysis
    [
        r"(.*) financial risk analysis",
        ["Financial risk analysis involves identifying and assessing the potential risks that could impact an organization's financial performance or objectives.",]
    ],
    [
        r"(.*) financial markets",
        ["Financial markets are platforms where individuals and institutions trade financial securities, commodities, and other fungible items at prices determined by supply and demand.",]
    ],
    [
        r"(.*) stock",
        ["A stock represents ownership in a corporation and entitles the owner to a share of the company's assets and profits.",]
    ],
    [
        r"(.*) bond",
        ["A bond is a fixed-income investment in which an investor loans money to an entity (typically a corporation or government) that borrows the funds for a defined period at a fixed interest rate.",]
    ],
    [
        r"(.*) credit ratings",
        ["Credit ratings are assessments of the creditworthiness of individuals, businesses, or securities based on their ability to repay debt obligations.",]
    ],
    
    # Corporate finance and valuation
    [
        r"(.*) company valuation",
        ["Company valuation is the process of determining the economic value of a business or its assets, typically for investment, acquisition, or financial reporting purposes.",]
    ],
    [
        r"(.*) capital budgeting",
        ["Capital budgeting is the process of evaluating and selecting long-term investment projects or expenditures that will generate future cash flows for a company.",]
    ],
    [
        r"(.*) financial modeling",
        ["Financial modeling is the process of creating a mathematical representation of a financial situation or business decision to analyze the impact of different variables and scenarios.",]
    ],
    [
        r"(.*) leveraged buyout",
        ["A leveraged buyout (LBO) is a financial transaction in which a company is acquired using a significant amount of borrowed money to meet the cost of acquisition.",]
    ],
    [
        r"(.*) financial derivatives",
        ["Financial derivatives are contracts whose value is derived from the performance of an underlying asset, index, or rate, such as options, futures, and swaps.",]
    ],
    
    # Forensic audit and fraud prevention
    [
        r"(.*) forensic audit",
        ["A forensic audit is an examination of financial records and transactions to uncover fraud, embezzlement, or other illegal activities.",]
    ],
    [
        r"(.*) insurance fraud",
        ["Insurance fraud involves deliberately deceiving an insurance company for financial gain, such as by filing false claims or providing misleading information.",]
    ],
    [
        r"(.*) anti-fraud measures",
        ["Anti-fraud measures are policies, procedures, and controls implemented by organizations to detect, prevent, and deter fraudulent activities.",]
    ],
    [
        r"(.*) whistleblower protection",
        ["Whistleblower protection laws are designed to protect individuals who report illegal or unethical behavior within an organization from retaliation or harassment.",]
    ],
    [
        r"(.*) fraud detection techniques",
        ["Fraud detection techniques include data analysis, forensic accounting, internal controls, and employee training to identify suspicious behavior or transactions.",]
    ],
    
    # Insurance-related queries
    [
        r"(.*) types of insurance",
        ["There are various types of insurance, including life insurance, health insurance, property insurance, liability insurance, and automobile insurance.",]
    ],
    [
        r"(.*) insurance premium",
        ["An insurance premium is the amount of money an individual or business pays to an insurance company in exchange for insurance coverage.",]
    ],
    [
        r"(.*) insurance claim",
        ["An insurance claim is a formal request made by a policyholder to an insurance company for compensation or coverage for a covered loss or event.",]
    ],
    [
        r"(.*) insurance policy",
        ["An insurance policy is a contract between an insurance company and a policyholder that outlines the terms and conditions of insurance coverage.",]
    ],
    [
        r"(.*) insurance coverage limits",
        ["Insurance coverage limits are the maximum amounts an insurance policy will pay for covered losses or events, as specified in the policy terms.",]
    ],
    
    # Financial planning and investment queries
    [
        r"(.*) retirement planning",
        ["Retirement planning involves setting financial goals and creating a savings and investment strategy to ensure a comfortable retirement.",]
    ],
    [
        r"(.*) investment portfolio diversification",
        ["Investment portfolio diversification is the practice of spreading investments across different asset classes, sectors, and geographic regions to reduce risk and maximize returns.",]
    ],
    [
        r"(.*) risk tolerance assessment",
        ["Risk tolerance assessment helps individuals and investors understand their willingness and ability to accept investment risk in pursuit of their financial goals.",]
    ],
    [
        r"(.*) financial goal setting",
        ["Financial goal setting involves identifying short-term and long-term objectives, such as saving for retirement, buying a home, or funding education, and creating a plan to achieve them.",]
    ],
    [
        r"(.*) tax-efficient investment strategies",
        ["Tax-efficient investment strategies aim to minimize taxes on investment income and capital gains through strategies such as tax-deferred accounts, tax-loss harvesting, and asset location optimization.",]
    ],
    
    # Accounting principles and standards
    [
        r"(.*) accounting principles",
        ["Accounting principles are the rules and guidelines that govern the preparation and presentation of financial statements, such as the accrual basis of accounting, revenue recognition principle, and matching principle.",]
    ],
    [
        r"(.*) international accounting standards",
        ["International accounting standards are a set of guidelines and rules issued by the International Accounting Standards Board (IASB) to ensure consistency and comparability in financial reporting across countries and industries.",]
    ],
    [
        r"(.*) compliance with accounting standards",
        ["Compliance with accounting standards requires companies to adhere to the principles and rules set forth by regulatory bodies such as the Financial Accounting Standards Board (FASB) or the International Financial Reporting Standards (IFRS) Foundation.",]
    ],
    [
        r"(.*) audit trail",
        ["An audit trail is a systematic record of the transactions and events that have occurred within an accounting system, providing a chronological history of financial activities and changes.",]
    ],
    [
        r"(.*) financial statement analysis",
        ["Financial statement analysis involves reviewing and interpreting a company's financial statements to assess its financial performance, liquidity, solvency, and profitability.",]
    ],

      # Default response
    [
        r"(.*)",
        ["I have not get your question,can you rephrase again?"]
    ],


]
# Default message at the start of chat
print("Hi , I am CA Chatbot and I like to chat \nPlease type lowercase English language to start a conversation. Type quit to leave.")

# Create Chat Bot
# chat.converse()


chat = Chat(pairs, reflections)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message')
    response = chat.respond(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
