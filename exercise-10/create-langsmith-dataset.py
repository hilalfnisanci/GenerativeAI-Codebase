import pandas as pd
from langsmith import Client

# QA
inputs = [
    "What are the salon's opening hours?",
    "Can I get an urgent haircut appointment for today?",
    "I want to file a complaint. I was very dissatisfied with my last haircut and I want a refund.",
    "Can I get information about women's haircut prices?",
    "Which hair care products do you use?",
    "I would like to make an appointment for a haircut.",
    "I lost my wallet in your salon, can I get information about lost and found items?",
    "I want my dog to get a haircut, can I make an appointment for my dog?",
    "Do you dye children's hair?",
    "I was very dissatisfied with the service I received yesterday."
]

outputs = [
    "Our salon's opening hours are as follows: \n\
- Monday: 10:15 AM - 5:00 PM \n- Tuesday: 10:15 AM - 5:00 PM \n- Wednesday: 10:15 AM - 5:00 PM \n- Thursday: 10:15 AM - 5:00 PM\n\
- Friday: 10:15 AM - 5:00 PM \n- Saturday: 10:15 AM - 4:00 PM\n\
Our salon is closed on Sundays and public holidays.",
    "Hello! I am the AI assistant of Nicholas Mark Hair Salon. I understand that you want to get an urgent haircut appointment. \
Could you please provide your name, phone number, and preferred appointment date?",
    "I am sorry to hear that you are unhappy with your last haircut. I will forward your message for further action. \
Could you please provide your name and contact information so I can assist you better?",
    "Hello, our prices for women's haircuts are as follows:\n\
- Cut and Wash & Blow Dry: £48.50\n\
- Wet Cut: £28.50\n\
- Curly Hair Cut: from £80\n\
For more information or to book an appointment, please contact us!",
    "At Nicholas Mark Hair Salon, we use various brands of hair care products. \
For example, we use Loreal Majirel for hair coloring, Indola for highlights, Yuko for permanent straightening, \
Kerastraight for Brazilian Blow Dry, and Schwarzkopf, Osmo, and Wella products for styling.",
    "Hello! I am the AI assistant of Nicholas Mark Hair Salon. \
I understand that you want to make an appointment for a haircut. Could you please provide your name, phone number, and preferred appointment date?",
    "Unfortunately, I cannot provide information about lost or found items in our salon. \
For better assistance, please call our salon directly at 0191 2619651. \
Is there anything else I can help you with?",
    "Hello! I am the AI assistant of Nicholas Mark Hair Salon. \
Unfortunately, our salon only serves human customers and does not offer grooming services for pets. \
Is there anything else I can help you with?",
    "Unfortunately, there is an age restriction for hair coloring services at our salon. \
A skin test must be conducted within 48 hours before the appointment, and the customer must be at least 16 years old for this test.",
    "I'm sorry to hear that you were dissatisfied with the service you received. \
Could you please share the details of the issue so I can assist you better?"
]

# Dataset
qa_pairs = [{"input" : q, "output" : a} for q, a in zip(inputs, outputs)]
df = pd.DataFrame(qa_pairs)

# Write to CSV
csv_path = "/your-path/agent_test_dataset.csv"
df.to_csv(csv_path, index=False)

client = Client()
dataset_name = "Nicholas-Mark-Hairdressing-Test-Dataset"

# Store
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="QA pairs about Nicholas Mark Hairdressing AI Assistant."
)
client.create_examples(
    inputs=[{"input":q} for q in inputs],
    outputs=[{"output":a} for a in outputs],
    dataset_id=dataset.id
)

inputs=[{"input":q} for q in inputs]
outputs=[{"output":a} for a in outputs]

print(inputs)

print("\n", outputs)
