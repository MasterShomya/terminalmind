import subprocess
import os
import sys
from typing import Annotated, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.live import Live
from rich.spinner import Spinner
import joblib
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog


load_dotenv()

# init rich's console
console = Console()

# Initialize chat history
chat_history = []

# file dialog helper
def _open_file_dialog(title: str, file_types: list[tuple[str, str]]) -> str:
    """
    Opens a native file explorer dialog to select a file.
    Hides the root tkinter window.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hides root window
        root.attributes('-topmost', True)  # Brings dialog to front
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=file_types
        )
        
        root.destroy()  # Cleans root window
        return file_path
    except Exception as e:
        console.print(f"[bold red]Error opening file dialog:[/bold red] {e}")
        # Tries to destroy root window if it still exists
        try:
            root.destroy()
        except:
            pass
        return ""

'''
 -----------------------------------------------------------------------------
 DON'T REMOVE THE COMMENTS INSIDE ANY FUNCTION WHICH IS DECORATED WITH '@tool'
 as it serves as a tool description and it helps LLM to choose the right tool
 -----------------------------------------------------------------------------
'''

# tools
@tool
def ipconfig() -> str:
    """
    Shows IP address, subnet mask, and default gateway for all network adapters.
    Use this when user asks about IP address, network configuration, or connection details.
    """
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing ipconfig: {str(e)}"


@tool
def netstat() -> str:
    """
    Lists all active network connections and listening ports.
    Use this when user asks about open connections, ports, or network activity.
    """
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing netstat: {str(e)}"


@tool
def arp_table() -> str:
    """
    Displays the ARP (Address Resolution Protocol) table showing IP to MAC address mappings.
    Use this when user asks about MAC addresses, device mapping, or local network devices.
    """
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing arp: {str(e)}"


@tool
def route_table() -> str:
    """
    Shows the routing table with network destinations and gateways.
    Use this when user asks about routing, network paths, or gateway information.
    """
    try:
        result = subprocess.run(['route', 'print'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing route print: {str(e)}"


@tool
def get_mac_addresses() -> str:
    """
    Shows MAC addresses for all network adapters.
    Use this when user specifically asks about MAC addresses of the computer.
    """
    try:
        result = subprocess.run(['getmac'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing getmac: {str(e)}"


@tool
def get_hostname() -> str:
    """
    Displays the computer's network hostname.
    Use this when user asks about computer name or hostname.
    """
    try:
        result = subprocess.run(['hostname'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing hostname: {str(e)}"


@tool
def wifi_profiles() -> str:
    """
    Lists all saved Wi-Fi network profiles on the computer.
    Use this when user asks about saved Wi-Fi networks or wireless profiles.
    """
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing netsh wlan show profiles: {str(e)}"


@tool
def wifi_interface_info() -> str:
    """
    Shows current Wi-Fi connection details including signal strength, SSID, and connection status.
    Use this when user asks about current Wi-Fi connection, signal strength, or wireless status.
    """
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing netsh wlan show interfaces: {str(e)}"


@tool
def system_info() -> str:
    """
    Displays detailed system and network configuration information.
    Use this when user asks about comprehensive system information, OS details, or full network config.
    """
    try:
        result = subprocess.run(['systeminfo'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing systeminfo: {str(e)}"


@tool
def list_directory() -> str:
    """
    Lists all files and folders in the current directory.
    Use this when user asks to see files, list directory contents, or show what's in current folder.
    """
    try:
        result = subprocess.run(['dir'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing dir: {str(e)}"


@tool
def current_directory() -> str:
    """
    Shows the current working directory path.
    Use this when user asks where they are, current location, or current directory.
    """
    try:
        result = subprocess.run(['cd'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing cd: {str(e)}"


@tool
def system_time() -> str:
    """
    Displays current system date and time.
    Use this when user asks about current time, date, or system clock.
    """
    try:
        result = subprocess.run(['time', '/t'], capture_output=True, text=True, shell=True)
        time_output = result.stdout
        result = subprocess.run(['date', '/t'], capture_output=True, text=True, shell=True)
        date_output = result.stdout
        return f"Date: {date_output}Time: {time_output}"
    except Exception as e:
        return f"Error executing time/date: {str(e)}"


@tool
def disk_info() -> str:
    """
    Shows disk drive information including free space and total size.
    Use this when user asks about disk space, storage, drive capacity, or how much space is left.
    """
    try:
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name,size,freespace'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing wmic logicaldisk: {str(e)}"


@tool
def running_processes() -> str:
    """
    Lists all currently running processes on the system.
    Use this when user asks about running programs, active processes, or what's running on the computer.
    """
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing tasklist: {str(e)}"


@tool
def environment_variables() -> str:
    """
    Shows all system environment variables.
    Use this when user asks about environment variables, PATH, or system variables.
    """
    try:
        result = subprocess.run(['set'], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return f"Error executing set: {str(e)}"

# ANOMALY DETECTION MODEL AS A TOOL
@tool
def run_anomaly_inference() -> str:
    """
    Runs anomaly detection inference using a pre-trained Isolation Forest model.
    Use this tool when the user asks to 'run inference', 'find anomalies',
    'check a file for anomalies', or 'run the model'.
    
    This tool will interactively ask the user to select two files using a file explorer:
    1. The pre-trained model file (e.g., 'isolation_forest_model.pkl').
    2. The CSV data file to perform inference on.
    
    The tool then:
    - Loads the model and the data.
    - Predicts anomalies (1 = anomaly, 0 = normal).
    - Saves a new 'results.csv' file in the *same directory* as the input data file.
    - Returns a success message with the path to the results file.
    """
    
    # 1. Get the model path
    console.print("[bold yellow]Please select your .pkl model file...[/bold yellow]")
    model_path = _open_file_dialog(
        title="Select your pre-trained .pkl model file",
        file_types=[("Pickle files", "*.pkl"), ("All files", "*.*")]
    )
    
    if not model_path:
        return "Inference cancelled. No model file selected."
    
    console.print(f"[dim]Model file selected:[/dim] {model_path}")

    # 2. Get the data path
    console.print("[bold yellow]Please select your .csv data file for inference...[/bold yellow]")
    data_path = _open_file_dialog(
        title="Select the .csv data file for inference",
        file_types=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not data_path:
        return "Inference cancelled. No data file selected."

    console.print(f"[dim]Data file selected:[/dim] {data_path}")

    try:
        # 3. Load model and data
        with console.status("[bold green]Running inference...[/bold green]", spinner="dots"):
            model = joblib.load(model_path)
            data = pd.read_csv(data_path)

            # 4. Predict
            preds = model.predict(data)
            preds = np.where(preds == -1, 1, 0)  # 1 = anomaly, 0 = normal

            # 5. Create results DataFrame
            results = pd.DataFrame({
                "prediction": preds,
                "status": ["Anomaly" if p == 1 else "Normal" for p in preds]
            })
            
            # 6. Define and save output
            output_dir = os.path.dirname(data_path)
            output_path = os.path.join(output_dir, "results.csv")
            
            results.to_csv(output_path, index=False)
        
        return f"Inference complete! Results saved successfully to: {output_path}"

    except Exception as e:
        console.print(f"[bold red]An error occurred during inference:[/bold red] {str(e)}")
        return f"Error during inference: {str(e)}. Please check the console and files."


# Collecting all tools
tools = [
    ipconfig, netstat, arp_table, route_table, get_mac_addresses,
    get_hostname, wifi_profiles, wifi_interface_info, system_info,
    list_directory, current_directory, system_time, disk_info,
    running_processes, environment_variables,
    run_anomaly_inference
]

# Initialize LLM with tool binding
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


def show_banner():
    """Display the startup banner"""
    console.print()
    
    # ASCII art title
    title = """
 _____                                                                                                       _____ 
( ___ )                                                                                                     ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ███╗   ███╗██╗███╗   ██╗██████╗  |   | 
 |   | ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ████╗ ████║██║████╗  ██║██╔══██╗ |   | 
 |   |    ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║         ██╔████╔██║██║██╔██╗ ██║██║  ██║ |   | 
 |   |    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║         ██║╚██╔╝██║██║██║╚██╗██║██║  ██║ |   | 
 |   |    ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝ |   | 
 |   |    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝  |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                                                     (_____)
    """
    
    console.print(title, style="bold cyan", justify="center")
    
    # Capabilities grid
    capabilities_text = """
[bold cyan]Network Tools[/bold cyan]
  • IP Configuration & Routing
  • Active Connections & Ports  
  • Wi-Fi Analysis & Profiles

[bold green]System Info[/bold green]
  • Running Processes
  • Disk Space & Storage
  • Environment Variables

[bold yellow]File System[/bold yellow]
  • Directory Listing
  • Current Path Info
  • System Time & Date
  
[bold magenta]AI / ML Models[/bold magenta]
  • Run Anomaly Detection
"""
    
    console.print(
        Panel(
            capabilities_text.strip(),
            title="[bold white]⚡ Capabilities[/bold white]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2)
        )
    )
    
    console.print(
        "\n[dim italic]💡 Ask me anything about your system - I'll figure out what to run![/dim italic]\n",
        justify="center"
    )


def run_agent(user_query: str):
    """Main agent function that processes user queries"""
    global chat_history
    
    # Add user message to history
    chat_history.append(HumanMessage(content=user_query))
    
    # Show thinking indicator
    with console.status("[bold cyan]Thinking...", spinner="dots"):
        # Get LLM response with tool selection
        response = llm_with_tools.invoke(chat_history)
    
    # Check if LLM wants to use a tool
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            
            # Show execution status
            console.print()
            console.print(
                f"[bold cyan]⚙[/bold cyan]  Executing [bold yellow]{tool_name}[/bold yellow]",
                style="dim"
            )
            
            # Find and execute the tool
            selected_tool = None
            for tool in tools:
                if tool.name == tool_name:
                    selected_tool = tool
                    break
            
            if selected_tool:
                # Execute the tool with spinner
                # Special handling for inference tool as it has its own printouts
                if tool_name == 'run_anomaly_inference':
                    tool_output = selected_tool.invoke({})
                else:
                    with console.status("[bold green]Running command...", spinner="dots"):
                        tool_output = selected_tool.invoke({})
                
                # Show command output in a collapsible panel
                output_preview = tool_output[:400] + ("..." if len(tool_output) > 400 else "")
                panel_title = "[green]✓[/green] Command Executed"
                if "Error" in tool_output or "cancelled" in tool_output:
                     panel_title = "[red]![/red] Command Finished"
                
                console.print(
                    Panel(
                        f"[dim]{output_preview}[/dim]",
                        title=panel_title,
                        subtitle=f"[dim]{len(tool_output)} characters[/dim]",
                        border_style="dim green",
                        box=box.ROUNDED,
                        padding=(0, 1)
                    )
                )
                
                # Add tool response to history
                chat_history.append(response)
                
                # Create a more targeted prompt for the LLM to summarize the tool output
                summary_prompt = f"""I just executed the '{tool_name}' command for you. Here's what it returned:

{tool_output}

Now respond in a conversational way:
1. First mention that you ran the command (or that it was cancelled/failed).
2. If it was successful, give a brief, focused explanation of the KEY findings (7-8 sentences max)
3. If it failed or was cancelled, just acknowledge that.
4. Only highlight what's most relevant to my question
5. Keep it natural and concise - don't dump everything
6. Keep it the way that you are really putting value by explaining the findings.

Be conversational and acknowledge you executed it!"""
                
                # For the inference tool, the output is already a summary, so we can use a simpler prompt
                if tool_name == 'run_anomaly_inference':
                    summary_prompt = f"""The '{tool_name}' tool finished running and returned this message:

{tool_output}

Acknowledge this message conversationally. If it was successful, congratulate the user and confirm where the results are. If it was cancelled or failed, just be helpful and ask if they'd like to try something else."""

                chat_history.append(HumanMessage(content=summary_prompt))
                
                # Get LLM explanation with spinner
                with console.status("[bold cyan]Analyzing results...", spinner="dots"):
                    final_response = llm.invoke(chat_history)
                
                # Render AI response beautifully
                ai_response_panel = Panel(
                    Markdown(final_response.content),
                    title="[bold cyan]🤖 TerminalMind[/bold cyan]",
                    border_style="cyan",
                    box=box.DOUBLE,
                    padding=(1, 2),
                    width=console.width - 4
                )
                console.print()
                console.print(ai_response_panel)
                console.print()
                
                # Add final response to history
                chat_history.append(final_response)
    else:
        # No tool needed, just respond
        ai_response_panel = Panel(
            Markdown(response.content),
            title="[bold cyan]🤖 TerminalMind[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2),
            width=console.width - 4
        )
        console.print()
        console.print(ai_response_panel)
        console.print()
        chat_history.append(response)


def main():
    """Main entry point for the CLI application"""
    try:
        # Clear screen for clean start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Show banner
        show_banner()
        
        # Main interaction loop
        while True:
            try:
                # Get user input with rich prompt
                user_input = Prompt.ask("\n[bold cyan]›[/bold cyan]").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
                    goodbye_panel = Panel(
                        "[bold cyan]Thanks for using TerminalMind![/bold cyan]\n[dim]See you next time 👋[/dim]",
                        border_style="cyan",
                        box=box.DOUBLE,
                        padding=(1, 2)
                    )
                    console.print()
                    console.print(goodbye_panel)
                    console.print()
                    break
                
                if not user_input:
                    continue
                
                # Process the query
                run_agent(user_input)
                
            except KeyboardInterrupt:
                goodbye_panel = Panel(
                    "[bold yellow]⚠ Interrupted[/bold yellow]\n[dim]Session ended[/dim]",
                    border_style="yellow",
                    box=box.DOUBLE,
                    padding=(1, 2)
                )
                console.print("\n")
                console.print(goodbye_panel)
                console.print()
                break
                
    except Exception as e:
        error_panel = Panel(
            f"[bold red]BYE-BYE:[/bold red]\n[dim]{str(e)}[/dim]",
            border_style="red",
            box=box.DOUBLE,
            padding=(1, 2)
        )
        console.print("\n")
        console.print(error_panel)
        console.print()
        sys.exit(1)


if __name__ == "__main__":
    main()