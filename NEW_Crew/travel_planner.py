import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.5,
    verbose=True,
    api_key=os.getenv("GOOGLE_API_KEY")
)

search_tool = SerperDevTool()

def generate_travel_plan(destination: str, budget: str):
    researcher = Agent(
        role="Travel Researcher",
        goal=f"Find historical sites, hotels, weather for {destination}",
        backstory="You are an expert travel researcher who provides high-quality and up-to-date travel information.",
        memory=True,
        llm=llm,
        tools=[search_tool],
        verbose=True,
        allow_delegation=True
    )

    budget_planner = Agent(
        role="Budget Planner",
        goal=f"Find hotels, flights, and costs for {destination} under ${budget}.",
        backstory="You are a skilled financial planner focused on helping travelers stay within budget while having a great experience.",
        llm=llm,
        tools=[search_tool],
        verbose=True
    )

    itinerary_planner = Agent(
        role="Itinerary Planner",
        goal=f"Create a 3-day itinerary for {destination} under ${budget}.",
        backstory="You are an expert in travel planning. You balance sightseeing, rest, and budget perfectly to craft enjoyable multi-day travel experiences.",
        llm=llm,
        tools=[search_tool],
        verbose=True
    )

    task1 = Task(description="Research historical sites, transport, and weather",expected_output="A list of top 5 historical sites, current 3-day weather forecast, and 3 hotel options near public transport.", agent=researcher)
    task2 = Task(description="Calculate budget costs including hotels and flights", expected_output="Flight cost, hotel cost, and estimated daily costs that keep the total under the user's budget.", agent=budget_planner)
    task3 = Task(description="Create a 3-day itinerary",expected_output="Day-wise plan with historical site visits, cost estimates, and transport details.", agent=itinerary_planner)

    crew = Crew(
        agents=[researcher, budget_planner, itinerary_planner],
        tasks=[task1, task2, task3],
        process=Process.sequential
    )

    result = crew.kickoff(inputs={"destination": destination, "budget": budget})
    return result
