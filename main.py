#Code By : http//t.me/PmOfBangladesh
#Channel: BetaTesterZone

import os
import subprocess
import time
import psutil
import sys
import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, 
    TimeRemainingColumn, TransferSpeedColumn
)
from rich.prompt import Prompt
from rich.align import Align
from rich import box

# initialize console
PmOfBangladesh_Console = Console()

class BetaTesterZone_Compressor:
    def __init__(self):
        self.BetaTesterZone_In = "/storage/emulated/0/Download"
        self.PmOfBangladesh_Out = "/storage/emulated/0/SML_Output"
        self.BetaTesterZone_Files = []
        
        if not os.path.exists("/storage/emulated/0"):
            self.BetaTesterZone_In = "/sdcard" 
            self.PmOfBangladesh_Out = "output"

    def BetaTesterZone_Clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def PmOfBangladesh_Banner(self):
        self.BetaTesterZone_Clear()
        # Updated Banner: Large SML Logo with VIDEO COMPRESSOR text
        title = """
[bold cyan]   _____ __  __ __      [/]
[bold cyan]  / ____|  \/  | |      [/][bold white] SML VIDEO[/]
[bold cyan] | (___ | \  / | |      [/][bold white] COMPRESSOR[/]
[bold cyan]  \___ \| |\/| | |      [/][bold yellow] [/]
[bold cyan]  ____) | |  | | |____  [/]
[bold cyan] |_____/|_|  |_|______| [/]
"""
        info_panel = f"""
[bold yellow]Input Folder  :[/][white] {self.BetaTesterZone_In}[/]
[bold yellow]Output Folder :[/][white] {self.PmOfBangladesh_Out}[/]
[bold cyan]Developed By  :[/][white] @PmOfBangladesh[/]
"""
        PmOfBangladesh_Console.print(Panel(Align.center(title + info_panel), border_style="cyan", box=box.DOUBLE))

    def BetaTesterZone_Ram(self):
        return f"{psutil.virtual_memory().percent}%"

    def PmOfBangladesh_Paths(self):
        self.PmOfBangladesh_Banner()
        PmOfBangladesh_Console.print("[bold underline]PATH CONFIGURATION[/]\n")
        new_in = Prompt.ask("[bold green]Enter Input Path[/]", default=self.BetaTesterZone_In)
        if os.path.isdir(new_in): self.BetaTesterZone_In = new_in
        
        new_out = Prompt.ask("[bold green]Enter Output Path[/]", default=self.PmOfBangladesh_Out)
        if not os.path.exists(new_out):
            try: os.makedirs(new_out); self.PmOfBangladesh_Out = new_out
            except: pass
        else: self.PmOfBangladesh_Out = new_out

    def BetaTesterZone_Scan(self):
        exts = ('.mp4', '.mkv', '.avi', '.mov', '.3gp', '.flv')
        try:
            self.BetaTesterZone_Files = [f for f in os.listdir(self.BetaTesterZone_In) if f.lower().endswith(exts)]
            self.BetaTesterZone_Files.sort()
        except: self.BetaTesterZone_Files = []

    def PmOfBangladesh_Select(self):
        self.BetaTesterZone_Scan()
        if not self.BetaTesterZone_Files:
            PmOfBangladesh_Console.print("[bold red]No video files found![/]")
            time.sleep(2)
            return None

        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Filename", style="white")
        table.add_column("Size", style="green", justify="right")

        for idx, f in enumerate(self.BetaTesterZone_Files):
            size_mb = os.path.getsize(os.path.join(self.BetaTesterZone_In, f)) / (1024 * 1024)
            table.add_row(str(idx + 1), f, f"{size_mb:.2f} MB")

        PmOfBangladesh_Console.print(table)
        selection = Prompt.ask("[bold yellow]Select (e.g. 1, 1-5, all)[/]")
        if selection.lower() == 'all': return self.BetaTesterZone_Files

        selected_indices = set()
        try:
            parts = selection.split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    for i in range(start, end + 1): selected_indices.add(i - 1)
                else:
                    selected_indices.add(int(part) - 1)
        except: return None
        return [self.BetaTesterZone_Files[i] for i in selected_indices if 0 <= i < len(self.BetaTesterZone_Files)]

    def BetaTesterZone_Settings(self):
        PmOfBangladesh_Console.print("\n[bold cyan]--- VIDEO RESOLUTION ---[/]")
        options = {
            "1": ("1080p (FHD)", "-1:1080", "modern"),
            "2": ("720p (HD)", "-1:720", "modern"),
            "3": ("480p (SD)", "-1:480", "modern"),
            "4": ("360p (Low)", "-1:360", "modern"),
            "5": ("Button Phone 1 (176x144)", "176:144", "legacy"),
            "6": ("Button Phone 2 (240x360)", "240:360", "legacy"),
        }
        
        for k, v in options.items():
            PmOfBangladesh_Console.print(f"{k}. [white]{v[0]}[/]")
        
        choice = Prompt.ask("Select Quality", choices=list(options.keys()), default="2")
        selected_res = options[choice]

        PmOfBangladesh_Console.print("\n[bold cyan]--- AUDIO CONFIGURATION ---[/]")
        PmOfBangladesh_Console.print("1. [white]128kbps (Standard)[/]\n2. [white]Original (Copy Audio)[/]\n3. [white]Mono (Low Bitrate)[/]")
        audio_choice = Prompt.ask("Select Audio", choices=["1", "2", "3"], default="1")

        audio_map = {
            "1": ["-c:a", "aac", "-b:a", "128k", "-ac", "2"],
            "2": ["-c:a", "copy"],
            "3": ["-c:a", "aac", "-b:a", "32k", "-ac", "1", "-ar", "22050"]
        }
        
        return {
            "ext": ".mp4",
            "scale": selected_res[1],
            "mode": selected_res[2],
            "audio": audio_map[audio_choice]
        }

    def PmOfBangladesh_Process(self):
        target_files = self.PmOfBangladesh_Select()
        if not target_files: return

        settings = self.BetaTesterZone_Settings()
        
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[filename]}"),
            BarColumn(bar_width=20),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TextColumn("[bold yellow]RAM: {task.fields[ram]}")
        )

        with progress:
            for filename in target_files:
                inp = os.path.join(self.BetaTesterZone_In, filename)
                out = os.path.join(self.PmOfBangladesh_Out, f"SML_{os.path.splitext(filename)[0]}{settings['ext']}")
                
                duration = 0
                try:
                    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", inp]
                    duration = float(subprocess.check_output(cmd_dur).decode().strip())
                except: pass

                task_id = progress.add_task("proc", filename=filename[:12], ram=self.BetaTesterZone_Ram(), total=100)

                cmd = ["ffmpeg", "-y", "-i", inp, "-vf", f"scale={settings['scale']}"]
                
                if settings['mode'] == 'modern':
                    cmd.extend(["-c:v", "libx264", "-crf", "24", "-preset", "faster"])
                else:
                    cmd.extend(["-c:v", "mpeg4", "-q:v", "7", "-r", "15", "-pix_fmt", "yuv420p"])

                cmd.extend(settings['audio'])
                cmd.extend(["-progress", "pipe:1", out])

                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                
                for line in proc.stdout:
                    if "out_time_ms=" in line:
                        try:
                            t = int(line.strip().split("=")[1]) / 1000000
                            if duration:
                                pct = (t / duration) * 100
                                progress.update(task_id, completed=pct, ram=self.BetaTesterZone_Ram())
                        except: pass
                
                proc.wait()
                progress.update(task_id, completed=100)

        PmOfBangladesh_Console.print("\n[bold green]✔ Processing Complete![/]")
        input("\nPress Enter to continue...")

    def BetaTesterZone_Run(self):
        while True:
            self.PmOfBangladesh_Banner()
            PmOfBangladesh_Console.print("[1] [bold green]Start Compression[/]")
            PmOfBangladesh_Console.print("[2] [bold yellow]Change Paths[/]")
            PmOfBangladesh_Console.print("[3] [bold red]Exit[/]")
            
            choice = Prompt.ask("\n[bold cyan]Select[/]", choices=["1", "2", "3"])
            
            if choice == "1": 
                self.PmOfBangladesh_Process()
            elif choice == "2": 
                self.PmOfBangladesh_Paths()
            elif choice == "3": 
                sys.exit()

if __name__ == "__main__":
    app = BetaTesterZone_Compressor()
    app.BetaTesterZone_Run()
