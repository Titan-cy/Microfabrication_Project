import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import os

# Tooltip Class with auto-wrap
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        frame = tk.Frame(tw, background='lightyellow', borderwidth=1, relief="solid")
        frame.pack()

        label = tk.Label(frame, text=self.text, justify='left',
                         background='lightyellow', font=("Arial", 10),
                         padx=10, pady=5, wraplength=200)
        label.pack()

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        if tw:
            tw.destroy()
        self.tooltip_window = None

def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class AnimatedGIF:
    def __init__(self, label, gif_path, width):
        self.label = label
        self.width = width
        self.gif_path = gif_path
        self.frames = []
        self.current_frame = 0
        self.animation = None
        
        try:
            img = Image.open(gif_path)
            for frame in ImageSequence.Iterator(img):
                frame = frame.copy()
                frame = frame.resize((width, int(width * frame.height / frame.width)), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.frames = [None]
            
        self.animate()
    
    def animate(self):
        if len(self.frames) > 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.label.configure(image=self.frames[self.current_frame])
            self.animation = self.label.after(100, self.animate)
    
    def stop(self):
        if self.animation:
            self.label.after_cancel(self.animation)
            self.animation = None

def load_local_image(image_path, width):
    try:
        if image_path.lower().endswith('.gif'):
            # For GIFs, we'll handle them separately
            img = Image.open(image_path)
            first_frame = next(ImageSequence.Iterator(img))
            first_frame = first_frame.resize((width, int(width * first_frame.height / first_frame.width)), Image.LANCZOS)
            return ImageTk.PhotoImage(first_frame)
        else:
            img = Image.open(image_path)
            img = img.resize((width, int(width * img.height / img.width)), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def open_litho_process():
    process_window = tk.Toplevel(root)
    process_window.title("Detailed Lithography Process with Visual Guides")
    process_window.geometry("1000x700")
    process_window.configure(bg='white')
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(process_window, bg='white')
    main_frame.pack(fill='both', expand=True)
    
    # Create canvas
    canvas = tk.Canvas(main_frame, bg='white')
    canvas.pack(side='left', fill='both', expand=True)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    
    # Configure canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    
    # Create another frame inside canvas
    content_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')
    
    # Bind mousewheel to the canvas for universal scrolling
    canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))
    
    # Title
    tk.Label(content_frame, 
             text="Comprehensive Lithography Process with Visual References", 
             font=("Arial", 16, "bold"), 
             bg='white').pack(pady=20)
    

    steps = [
        ("1. Substrate Preparation", 
         """The lithography process begins with meticulous wafer cleaning - the foundation for all subsequent steps. Using the industry-standard RCA cleaning method, wafers undergo a two-stage purification process: first removing organic contaminants with an ammonia-peroxide solution, then eliminating metallic ions with a hydrochloric acid mixture. 

The science behind this: These solutions create chemical reactions that lift contaminants from the silicon surface without damaging its crystalline structure. Megasonic cleaning (high-frequency sound waves) then removes nanoparticles, while spin-rinse-drying leaves an atomically smooth surface. 

Why it matters: Even nanometer-scale impurities can disrupt circuit patterns. This cleaning ensures perfect photoresist adhesion and pattern fidelity in later steps.
         
         The substrate preparation begins with a thorough cleaning sequence:
         • RCA Standard Clean 1 (SC-1): 5:1:1 H2O:H2O2:NH4OH at 75°C ±2°C for 10min
         • Megasonic DI rinse: 1MHz frequency, 20°C ±1°C for 3min
         • RCA Standard Clean 2 (SC-2): 6:1:1 H2O:H2O2:HCl at 75°C ±2°C for 10min
         • Final rinse: Overflow DI water (18.2MΩ·cm) for 5min
         • Spin-rinse-dry: 2000rpm for 60s with N2 purge""",
         "step1_substrate.png"),

        ("2. HMDS Priming", 
         """Before photoresist application, wafers receive an HMDS primer that transforms the surface chemistry. In a vacuum chamber, HMDS vapor reacts with surface hydroxyl groups to create a hydrophobic monolayer.

The chemistry at work: Si-OH + HMDS → Si-O-Si(CH₃)₃ + NH₃. This reaction changes the wafer from water-attracting to water-repelling, much like waxing a car. 

Practical importance: This invisible layer (just 1-2 molecules thick) prevents resist beading and ensures uniform coating. Modern systems integrate this step with coating tracks to maintain cleanroom conditions throughout.
         
         HMDS vapor priming process details:
         Equipment: SVG Coat Track with vacuum vapor prime module
         Process Sequence:
         1. Dehydration bake: 150°C ±1°C for 60s (hotplate)
         2. Vacuum pump down: 30s to 50Torr ±5Torr
         3. HMDS vapor dose: 5ml liquid HMDS vaporized at 23°C
         4. Reaction time: 45s ±5s at 50Torr
         5. Vent to N2 atmosphere: 20s ramp to 760Torr

         Chemical Reaction:
         Si-OH (surface) + (CH3)3Si-NH-Si(CH3)3 → 2 Si-O-Si(CH3)3 + NH3↑""",
         "step2_hmds.png"),

        ("3. Photoresist Coating", 
         """A light-sensitive polymer solution is spin-coated onto the wafer, forming an ultra-thin, uniform film. The spinning process has two phases: initial low-speed spread (500-1000 rpm) followed by high-speed thinning (1000-5000 rpm).

Physics principle: Centrifugal force (F=mω²r) distributes the resist outward while solvent evaporation leaves a solid film. The thickness follows t = kω^α, where faster spins create thinner films.

Key considerations: Processing occurs under yellow light to prevent premature exposure. Resist is filtered to 0.1μm to remove particles that could cause defects in the nanoscale patterns.
         
         Spin coating specifications for i-line resist:
         Resist: AZ® 5214E (positive tone)
         Process Parameters:
         • Dispense: 3ml resist at 500rpm (static dispense)
         • Spread: 1000rpm for 3s (accel 10,000rpm/s²)
         • Spin: 4000rpm for 30s (final thickness 1.4μm)
         • Edge bead removal: 1mm edge, solvent spray""",
         "step3_coating.gif"),

        ("4. Soft Bake", 
         """A gentle bake removes residual solvents and stabilizes the resist film. Modern systems use precisely controlled hotplates with proximity gap technology to ensure uniform heating.

What happens at the molecular level: Polymer chains rearrange and condense, increasing the glass transition temperature (Tg). About 10-30% thickness is lost as solvents evaporate.

Process balance: Temperature must be high enough to remove solvents but low enough to prevent premature degradation of the photosensitive compounds. The sweet spot is typically 90-110°C.
         
         Post-apply bake thermal profile:
         Equipment: In-line hotplate with proximity gap
         Temperature Zones:
         1. Ramp-up: 23°C to 100°C in 30s (2.5°C/s)
         2. Soak: 100°C ±0.3°C for 60s
         3. Ramp-down: 100°C to 23°C in 45s

         Process Window:
         • Minimum temp: 95°C (incomplete solvent removal)
         • Maximum temp: 105°C (resist degradation)
         • Optimal range: 98-102°C""",
         "step4_softbake.png"),

        ("5. Exposure", 
         """The magic of pattern transfer occurs here. Ultraviolet light projects the circuit design through a photomask onto the resist. Modern systems achieve incredible precision - aligning multiple wafer layers within nanometers.

Optical science: Different wavelengths (g-line 436nm to EUV 13.5nm) enable various feature sizes. The aerial image quality depends on numerical aperture and coherence factor.

Advanced techniques: Optical Proximity Correction (OPC) accounts for light diffraction effects, adding tiny adjustments to the mask pattern so it prints correctly on the wafer.
         
         """,
         "step5_exposure.png"),

        ("6. PEB", 
         """For chemically amplified resists, this bake triggers the crucial chemical reactions that develop the latent image. Heat causes acid molecules to diffuse and catalyze polymer deprotection.

Reaction dynamics: Acid concentration follows [H⁺]=[H⁺]₀e^(-Ea/RT), with diffusion length carefully controlled (typically 10-50nm). Temperature uniformity must be within ±0.1°C across the wafer.

Critical timing: The "PEB delay" between exposure and baking must be minimized (<60s) to prevent atmospheric contaminants from neutralizing the active acid compounds.
         
         Post-exposure bake specifications:
         Equipment: Track-mounted multi-zone hotplate
         Thermal Profile:
         • Ramp-up: 23°C to 110°C in 15s (5.8°C/s)
         • Soak: 110°C ±0.1°C for 60s
         • Ramp-down: 110°C to 23°C in 20s""",
         "step6_peb.png"),

        ("7. Development", 
         """The developer solution washes away exposed resist areas (for positive tone), revealing the 3D circuit pattern. Standard developers use tetramethylammonium hydroxide (TMAH) in precise concentrations.

Process control: Development rate follows R = R₀ + A[H⁺]ⁿ, highly sensitive to temperature (±0.5°C control needed). Megasonic agitation helps develop small features without pattern collapse.

Visualization: Like photographic development, this transforms the invisible latent image into visible structures, creating the stencil for subsequent etching.
         """,
         "step7_develop.gif"),

        ("8. Hard Bake", 
         """A final bake strengthens the remaining resist pattern before etching. This crosslinks polymer chains, improving etch resistance by 20-50%.

Thermal effects: While beneficial for stability, baking causes slight resist flow (5-20nm critical dimension change) that must be accounted for in mask design.

Advanced solutions: Some processes use UV curing instead of thermal baking to minimize dimensional changes for the most advanced nodes.
         
         Final bake specifications:
         Equipment: Convection oven with N2 purge
         Thermal Profile:
         • Ramp-up: 23°C to 125°C in 5min (0.34°C/s)
         • Soak: 125°C ±1°C for 30min
         • Ramp-down: 125°C to 23°C in 10min

         """,
         "step8_hardbake.png"),

        ("9. Etching", 
         """The resist pattern now guides the etching of underlying layers. Plasma etching uses energized ions (like CF₄⁺ or Cl⁺) to physically and chemically remove exposed material.

Precision requirements: Etching must be anisotropic (vertical sidewalls), selective to the resist mask, and uniform across the wafer. Modern systems use real-time optical emission spectroscopy to detect endpoint.

Visual analogy: Like sandblasting through a stencil, this permanently transfers the temporary resist pattern into the actual device layers.
         
         Pattern transfer etch process:
         Equipment: Lam Research 2300 Kiyo
         Etch Chemistry:
         • Silicon: HBr/Cl2/O2 (40/20/5sccm)
         • Oxide: C4F8/Ar/O2 (30/50/5sccm)
         • Metal: Cl2/BCl3 (30/10sccm)


         Selectivity:
         • Resist:Si = 1:3
         • Resist:SiO2 = 1:4
         • Resist:Al = 1:5""",
         "step9_etch.gif"),

        ("10. Strip & Clean", 
         """Finally, all remaining resist is completely removed. Options include wet chemical stripping or oxygen plasma ashing, often combined for best results.

Cleaning science: Post-strip cleaning removes any residues that could interfere with subsequent processing. The water break test (observing how water beads on the surface) confirms perfect cleanliness.

Finished result: The wafer now bears the precise circuit patterns and is ready for the next manufacturing steps, such as deposition of additional layers.
         
         Resist removal process:
         Two-Stage Removal:
         1. Plasma ash: O2 (500sccm) at 250°C, 300W for 2min
         2. Wet clean: EKC265™ at 85°C for 10min

         Final Cleaning:
         • SC1: 5min at 70°C
         • Megasonic: 1MHz for 3min
         • Marangoni dry: IPA vapor + N2 knife""",
         "step10_strip.png")
    ]

    # Base directory for images 
    image_dir = "litho_images"  
    
    for step_num, step_desc, img_filename in steps:
        step_frame = tk.Frame(content_frame, bg='white', padx=10, pady=5)
        step_frame.pack(fill='x', padx=20, pady=10)
        
        # Step title
        title_frame = tk.Frame(step_frame, bg='white')
        title_frame.pack(anchor='w')
        tk.Label(title_frame, text=step_num, 
                font=("Arial", 14, "bold"), 
                bg='white').pack(side='left')
        
        # Content frame for image + description
        content_frame_inner = tk.Frame(step_frame, bg='white')
        content_frame_inner.pack(fill='x')
        
        # Description with improved formatting
        desc_frame = tk.Frame(content_frame_inner, bg='white')
        desc_frame.pack(side='left', fill='both', expand=True)
        
        text_widget = tk.Text(desc_frame, 
                            font=("Arial", 10), 
                            bg='white', 
                            wrap='word', 
                            width=60, 
                            height=40,
                            padx=5,
                            pady=5,
                            relief='flat')
        text_widget.insert('end', step_desc)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        # Load and display local image (now on right side)
        img_path = os.path.join(image_dir, img_filename)
        if os.path.exists(img_path):
            if img_filename.lower().endswith('.gif'):
                # Create a label for the GIF
                gif_label = tk.Label(content_frame_inner, bg='white')
                gif_label.pack(side='right', padx=10)
                # Create the animated GIF
                AnimatedGIF(gif_label, img_path, 350)
            else:
                img = load_local_image(img_path, 350)  # Adjust width as needed
                if img:
                    img_label = tk.Label(content_frame_inner, image=img, bg='white')
                    img_label.image = img  # Keep reference
                    img_label.pack(side='right', padx=10)
        
        # Separator
        ttk.Separator(step_frame, orient='horizontal').pack(fill='x', pady=10)
    
    # Close button
    ttk.Button(content_frame, 
               text="Close", 
               command=process_window.destroy).pack(pady=20)
    
    # Unbind when window closes
    process_window.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all('<MouseWheel>'), process_window.destroy()])
    
    

def open_char_process():
    """Detailed theoretical explanation of I-V and C-V characterization"""
    process_window = tk.Toplevel(root)
    process_window.title("I-V & C-V Characterization Theory")
    process_window.geometry("1200x850")
    process_window.configure(bg='white')
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(process_window, bg='white')
    main_frame.pack(fill='both', expand=True)
    
    # Create canvas
    canvas = tk.Canvas(main_frame, bg='white')
    canvas.pack(side='left', fill='both', expand=True)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    
    # Configure canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    
    # Create another frame inside canvas
    content_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')
    
    # Bind mousewheel to the canvas for universal scrolling
    canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))
    
    # Title
    tk.Label(content_frame, 
             text="Comprehensive Characterization Techniques", 
             font=("Arial", 16, "bold"), 
             bg='white').pack(pady=20)

    # Characterization steps data
    char_steps = [
        ("1. I-V Characterization Fundamentals",
         """PHYSICAL PRINCIPLES:
Current-Voltage (I-V) measurements reveal the charge transport mechanisms governing device operation:

1. Thermionic Emission (Forward Bias):
   - Carriers gain sufficient thermal energy to overcome the potential barrier
   - Exponential current increase with voltage (ideal diode equation)
   - Non-idealities manifest through:
     * Recombination in depletion region (n ≈ 2)
     * Series resistance effects (high current roll-off)
     * Tunneling contributions (high doping)

2. Space-Charge Limited Current (SCLC):
   - Dominates in low-mobility materials
   - Current limited by injected charge screening
   - Three regimes:
     Ohmic (J ∝ V) → Trap-filled limit → Child's law (J ∝ V²)

3. Reverse Bias Characteristics:
   - Generation current in depletion region
   - Trap-assisted tunneling (Poole-Frenkel effect)
   - Avalanche breakdown at high fields

MEASUREMENT CONSIDERATIONS:
- Voltage sweep direction affects trap charging
- Temperature dependence reveals activation energies
- Light illumination separates photoconduction effects""",
         "iv_theory.png"),

        ("2. C-V Characterization Physics",
         """CAPACITANCE MECHANISMS:
Capacitance-Voltage (C-V) measurements probe charge distribution dynamics:

1. Depletion Capacitance:
   - Space charge region acts as dielectric
   - Width varies with applied bias (C ∝ 1/√V)
   - Doping profile extracted from C⁻² vs V slope

2. Interface State Response:
   - Traps follow AC signal at low frequencies
   - Freeze out at high frequencies (1MHz)
   - Conductance method measures trap time constants

3. Deep Level Transients:
   - Capacitance transients after voltage steps
   - Emission rate depends on temperature:
     eₙ = σₙvₜₕNₛexp(-ΔE/kT)""",
         "cv_theory.png"),

        ("3. Parameter Extraction Methodology",
         """I-V ANALYSIS:
1. Ideality Factor (n):
   - Slope of ln(I) vs V plot
   - n = (q/kT)(dV/dlnI)
   - n=1: Pure thermionic emission
   - n=2: Dominant recombination

2. Series Resistance (Rₛ):
   - High current deviation from ideal
   - Rₛ = dV/dI - nkT/qI
   - Corrected voltage V' = V - IRₛ

C-V ANALYSIS:
1. Doping Concentration:
   - N = 2/(qεA²d(1/C²)/dV
   - Depth profile from incremental analysis

2. Flatband Voltage:
   - V_fb = Φₘₛ - Qₜₜ/Cₒₓ
   - Determines fixed charge density""",
         "analysis_methods.png"),

        ("4. Practical Measurement Considerations",
         """SYSTEM REQUIREMENTS:
1. I-V Measurement:
   - Source-measure unit (SMU) with:
     * Current resolution < 1pA
     * Voltage resolution < 1mV
   - Guarded connections for leakage control
   - Temperature-controlled stage

2. C-V Measurement:
   - LCR meter with:
     * 1mHz-10MHz frequency range
     * 1fF capacitance resolution
   - DC bias superposition capability
   - RF shielding for low-noise

ERROR SOURCES:
1. I-V Artifacts:
   - Self-heating at high currents
   - Photocurrent from ambient light
   - Non-equilibrium conditions (fast sweeps)

2. C-V Artifacts:
   - Series resistance effects
   - Minority carrier response
   - Deep level transient interference

BEST PRACTICES:
1. For I-V:
   - Use 4-wire Kelvin connections
   - Sweep rates < 100mV/s
   - Temperature stabilization (±0.1K)

2. For C-V:
   - Start from accumulation
   - Multiple frequency measurements
   - Wait for steady-state (τ > 10×measurement)""",
         "measurement_setup.png")
    ]


    # Base directory for characterization images
    char_image_dir = "char_images"  
    
    for step_num, step_desc, img_filename in char_steps:
        step_frame = tk.Frame(content_frame, bg='white', padx=10, pady=5)
        step_frame.pack(fill='x', padx=20, pady=10)
        
        # Step title
        title_frame = tk.Frame(step_frame, bg='white')
        title_frame.pack(anchor='w')
        tk.Label(title_frame, text=step_num, 
                font=("Arial", 14, "bold"), 
                bg='white').pack(side='left')
        
        # Content frame for image + description
        content_frame_inner = tk.Frame(step_frame, bg='white')
        content_frame_inner.pack(fill='x')
        
        # Description with improved formatting
        desc_frame = tk.Frame(content_frame_inner, bg='white')
        desc_frame.pack(side='left', fill='both', expand=True)
        
        text_widget = tk.Text(desc_frame, 
                            font=("Arial", 10), 
                            bg='white', 
                            wrap='word', 
                            width=60, 
                            height=40,
                            padx=5,
                            pady=5,
                            relief='flat')
        text_widget.insert('end', step_desc)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        # Load and display local image (now on right side)
        img_path = os.path.join(char_image_dir, img_filename)
        if os.path.exists(img_path):
            if img_filename.lower().endswith('.gif'):
                # Create a label for the GIF
                gif_label = tk.Label(content_frame_inner, bg='white')
                gif_label.pack(side='right', padx=10)
                # Create the animated GIF
                AnimatedGIF(gif_label, img_path, 350)
            else:
                img = load_local_image(img_path, 350)
                if img:
                    img_label = tk.Label(content_frame_inner, image=img, bg='white')
                    img_label.image = img
                    img_label.pack(side='right', padx=10)
        
        ttk.Separator(step_frame, orient='horizontal').pack(fill='x', pady=10)
    
    # Close button
    ttk.Button(content_frame, 
               text="Close", 
               command=process_window.destroy).pack(pady=20)
    
    # Unbind when window closes
    process_window.protocol("WM_DELETE_WINDOW", 
                          lambda: [canvas.unbind_all('<MouseWheel>'), 
                                 process_window.destroy()])


def create_tech_window(title, description, image_name, image_dir="litho_images"):
    tech_window = tk.Toplevel(root)
    tech_window.title(title)
    tech_window.geometry("900x650")  # Reduced window size
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(tech_window, bg='white')
    main_frame.pack(fill='both', expand=True)
    
    canvas = tk.Canvas(main_frame, bg='white')
    canvas.pack(side='left', fill='both', expand=True)
    
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Create content frame inside canvas
    content_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=content_frame, anchor='nw')
    
    # Title at the top
    title_label = tk.Label(content_frame, 
                         text=title, 
                         font=("Arial", 16, "bold"), 
                         bg='white')
    title_label.pack(pady=10, anchor='nw')  # Anchored to northwest
    
    # Content frame for image + description
    content_inner = tk.Frame(content_frame, bg='white')
    content_inner.pack(fill='both', expand=True, anchor='nw')  # Anchored to northwest
    
    # Text widget with proper sizing
    text_frame = tk.Frame(content_inner, bg='white')
    text_frame.pack(side='left', fill='both', expand=True, anchor='nw')
    
    text_widget = tk.Text(text_frame, 
                        font=("Arial", 10), 
                        bg='white', 
                        wrap='word', 
                        width=60,  # Reduced width
                        height=25,  # Fixed height
                        padx=10,
                        pady=10,
                        relief='flat')
    text_widget.insert('end', description)
    text_widget.config(state='disabled')
    
    # Add scrollbar for text widget
    text_scroll = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
    text_widget.configure(yscrollcommand=text_scroll.set)
    text_scroll.pack(side='right', fill='y')
    text_widget.pack(side='left', fill='both', expand=True)
    
    # Load and display image on right
    img_path = os.path.join(image_dir, image_name)
    if os.path.exists(img_path):
        img = load_local_image(img_path, 300)  # Reduced image size
        if img:
            img_label = tk.Label(content_inner, image=img, bg='white')
            img_label.image = img
            img_label.pack(side='right', padx=10, anchor='ne')  # Anchored to northeast
    
    # Close button at bottom
    close_btn = ttk.Button(content_frame, 
                         text="Close", 
                         command=tech_window.destroy)
    close_btn.pack(pady=10, anchor='s')  # Anchored to south
    
    # Update scrollregion after window is drawn
    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
        canvas.unbind('<Configure>')  # Only need to do this once
    
    canvas.bind('<Configure>', update_scrollregion)
    
    # Bind mousewheel for scrolling
    canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))
    tech_window.protocol("WM_DELETE_WINDOW", 
                       lambda: [canvas.unbind_all('<MouseWheel>'), 
                              tech_window.destroy()])

# Lithography Technique Windows
def open_optical_litho():
    description = """OPTICAL LITHOGRAPHY: The Workhorse of Semiconductor Patterning

Fundamentals:
Optical lithography uses light to transfer geometric patterns from a photomask to a light-sensitive photoresist. It's the dominant patterning technology in semiconductor manufacturing.

Key Components:
• Light Source: Mercury lamps (g-line 436nm, i-line 365nm) or excimer lasers (DUV 248nm, 193nm)
• Photomask: Chrome patterns on quartz substrate (4x or 5x magnification)
• Projection Optics: High-NA lenses (NA up to 1.35 with immersion)
• Photoresist: Chemically amplified resists for advanced nodes

Resolution Equation:
R = k₁·λ/NA
Where:
R = minimum feature size
λ = wavelength (nm)
NA = numerical aperture
k₁ = process factor (typically 0.25-0.4)

Modern Advancements:
• Immersion Lithography: Uses water between lens and wafer (NA > 1.0)
• Multiple Patterning: LELE, SADP, SAQP for <20nm features
• Computational Lithography: OPC, ILT, SMO for better pattern fidelity

Process Parameters:
• Alignment accuracy: <3nm (3σ)
• Overlay control: <2nm
• Depth of focus: 100-300nm
• Throughput: 100-200 wafers/hour
• Defect density: <0.01/cm²

Applications:
• CMOS logic devices
• Memory chips (DRAM, NAND)
• MEMS devices
• Advanced packaging"""
    create_tech_window("Optical Lithography", description, "optical_litho.png")

def open_ebeam_litho():
    description = """ELECTRON-BEAM LITHOGRAPHY: Ultimate Resolution Patterning

Fundamentals:
E-beam lithography uses a focused electron beam to directly write patterns on resist-coated substrates, achieving ultra-high resolution (<10nm).

Key Advantages:
• No physical masks required (direct-write)
• Exceptional resolution (5-10nm features)
• Excellent overlay accuracy (<2nm)
• Flexible pattern changes

Challenges:
• Very slow throughput (hours per wafer)
• Proximity effects from electron scattering
• High equipment and maintenance costs
• Resist sensitivity limitations

Technical Specifications:
• Beam energy: 10-100keV
• Beam current: 10pA-100nA
• Spot size: 1-5nm
• Positioning accuracy: <1nm
• Field size: 100-500μm
• Resist sensitivity: 10-100μC/cm²

Resolution Factors:
• Electron scattering (forward/backscatter)
• Resist contrast and sensitivity
• Beam blur and stability
• Pattern density effects

Applications:
• Photomask fabrication
• Research and development
• Quantum devices
• Photonic crystals
• Nanotechnology structures"""
    create_tech_window("Electron-beam Lithography", description, "ebeam_litho.png")

def open_nanoimprint_litho():
    description = """NANOIMPRINT LITHOGRAPHY: High-Throughput Nanoscale Patterning

Fundamentals:
NIL physically molds resist using a rigid template, enabling high-resolution patterning without complex optics.

Process Variants:
1. Thermal NIL: Heat resist above Tg, imprint, then cool
2. UV-NIL: UV-curable resist with transparent template
3. Roll-to-Roll: Continuous imprinting for flexible substrates

Key Advantages:
• Sub-10nm resolution demonstrated
• High throughput potential
• Lower cost than optical/EUV
• 3D patterning capability

Technical Specifications:
• Resolution: <10nm demonstrated
• Alignment accuracy: <5nm
• Throughput: >20 wafers/hour
• Template life: >1000 imprints
• Residual layer: <10nm uniformity

Challenges:
• Defect control
• Template fabrication
• Release agents required
• Pattern fidelity maintenance

Applications:
• NAND flash memory
• Bit-patterned media
• Photonic devices
• Biological applications
• Flexible electronics"""
    create_tech_window("Nanoimprint Lithography", description, "nanoimprint.png")

def open_xray_litho():
    description = """X-RAY LITHOGRAPHY: High-Energy Pattern Transfer

Fundamentals:
Uses synchrotron radiation (0.5-4nm wavelength) to pattern thick resists through proximity printing.

Key Features:
• Deep penetration through resist
• Minimal diffraction effects
• High aspect ratio patterns
• Parallel exposure of entire wafer

Technical Specifications:
• Wavelength: 0.5-4nm (typically 1nm)
• Mask-to-wafer gap: 10-50μm
• Resist thickness: Up to 1mm
• Aspect ratio: >50:1 demonstrated
• Exposure dose: 100-1000mJ/cm²

Advantages:
• No optical distortions
• High depth of focus
• Suitable for 3D structures
• Good for high-Z materials

Challenges:
• Mask fabrication difficulty
• Synchrotron access required
• Alignment challenges
• Limited to certain applications

Applications:
• MEMS devices
• LIGA process
• High-aspect ratio structures
• X-ray optics fabrication
• Biomedical devices"""
    create_tech_window("X-ray Lithography", description, "xray_litho.gif")

def open_uv_litho():
    description = """UV LITHOGRAPHY: Versatile Mid-Range Patterning

Fundamentals:
Utilizes ultraviolet light (300-400nm) for resist exposure, balancing resolution and throughput.

Key Features:
• Mercury lamp sources (g-line 436nm, i-line 365nm)
• Contact/proximity or projection modes
• Mature, reliable technology
• Cost-effective for many applications

Technical Specifications:
• Resolution: 0.5-1.0μm (projection)
• Depth of focus: 1-2μm
• Alignment accuracy: 50-100nm
• Throughput: 50-100 wafers/hour
• Resist thickness: 0.5-2.0μm

Process Considerations:
• Diffraction effects significant
• Contact mode causes mask damage
• Proximity gap affects resolution
• Resist selection critical

Advantages:
• Lower cost than DUV/EUV
• Simple operation
• Good for non-critical layers
• Wide resist compatibility

Applications:
• MEMS fabrication
• Microfluidics
• PCB manufacturing
• Displays
• Non-semiconductor patterning"""
    create_tech_window("UV Lithography", description, "uv_litho.gif")

# Characterization Technique Windows
def open_sem_analysis():
    description = """SCANNING ELECTRON MICROSCOPY (SEM): High-Resolution Surface Imaging

Fundamentals:
SEM uses a focused electron beam to scan samples, producing high-resolution images from emitted secondary electrons.

Key Capabilities:
• Resolution: 0.5-5nm (depending on instrument)
• Magnification: 10x-1,000,000x
• Depth of field: 10-100× better than optical
• Elemental analysis via EDS

Operating Principles:
1. Electron beam (1-30keV) scans sample surface
2. Secondary electrons emitted from surface
3. Signal intensity varies with surface topography
4. Backscattered electrons provide Z-contrast

Instrument Parameters:
• Accelerating voltage: 1-30kV
• Probe current: 1pA-100nA
• Working distance: 2-10mm
• Vacuum: 10⁻³ to 10⁻⁶ Pa
• Detector types: SE, BSE, EDS

Sample Requirements:
• Conductivity: Conductive or coated
• Size: Typically <1cm
• Vacuum compatibility required
• Dry, clean surface preferred

Applications:
• Semiconductor defect analysis
• Nanomaterial characterization
• Biological imaging (after preparation)
• Failure analysis
• Metrology"""
    create_tech_window("Scanning Electron Microscopy", description, "sem_microscope.png", "char_images")

def open_afm_analysis():
    description = """ATOMIC FORCE MICROSCOPY (AFM): Nanoscale Surface Profiling

Fundamentals:
AFM measures surface topography by scanning a sharp tip across the sample while monitoring tip-sample interactions.

Operating Modes:
1. Contact Mode: Tip in constant contact
2. Tapping Mode: Tip oscillates near surface
3. Non-contact Mode: Measures van der Waals forces

Key Specifications:
• Resolution: Atomic vertical, 1nm lateral
• Scan range: 1μm to 100μm
• Force sensitivity: <1nN
• Environment: Air, liquid, or vacuum

Measurement Capabilities:
• Topography (3D surface profile)
• Roughness (Ra, Rq, Rz)
• Mechanical properties (modulus, adhesion)
• Electrical properties (conductivity, potential)
• Magnetic properties

Advantages:
• Atomic-level resolution
• No sample coating required
• Works in various environments
• Quantitative height data

Limitations:
• Slow scan speed
• Tip convolution effects
• Limited field of view
• Sample damage possible

Applications:
• Surface roughness measurement
• Nanostructure characterization
• Biological samples
• Thin film analysis
• Semiconductor metrology"""
    create_tech_window("Atomic Force Microscopy", description, "afm_diagram.png", "char_images")

def open_xrd_analysis():
    description = """X-RAY DIFFRACTION (XRD): Crystal Structure Analysis

Fundamentals:
XRD measures diffraction patterns from crystalline materials to determine atomic structure and phase composition.

Key Techniques:
1. Powder XRD: Polycrystalline samples
2. Thin Film XRD: Grazing incidence
3. High-Resolution XRD: Rocking curves
4. XRR: Reflectivity for thin films

Information Obtained:
• Crystal structure identification
• Lattice parameters
• Crystallite size
• Strain/stress analysis
• Texture/preferred orientation

Instrument Parameters:
• X-ray source: Cu Kα (1.54Å) typical
• Detector: Point, linear, or 2D
• Angular range: 5-140° 2θ
• Resolution: <0.01° 2θ

Data Analysis:
• Peak position → d-spacing
• Peak width → crystallite size
• Peak intensity → texture
• Peak shifts → strain

Applications:
• Phase identification
• Thin film characterization
• Quality control
• Semiconductor epitaxy
• Materials research"""
    create_tech_window("X-ray Diffraction", description, "xrd_equipment.png", "char_images")

def open_raman_analysis():
    description = """RAMAN SPECTROSCOPY: Molecular Vibrational Fingerprinting

Fundamentals:
Measures inelastic scattering of light to probe molecular vibrations and crystal phonons.

Key Features:
• Chemical identification
• Crystal structure analysis
• Strain measurement
• Temperature mapping
• Non-destructive

Technical Specifications:
• Excitation wavelength: 325-785nm
• Resolution: <1cm⁻¹
• Spatial resolution: ~1μm
• Depth profiling capability
• Mapping/imaging possible

Information Obtained:
• Chemical bonds present
• Crystal phases
• Stress/strain state
• Defect density
• Layer thickness

Advantages:
• Minimal sample prep
• Works through transparent media
• No vacuum required
• Complementary to FTIR

Applications:
• Material identification
• Carbon nanotube characterization
• Semiconductor strain analysis
• Pharmaceutical analysis
• Art conservation"""
    create_tech_window("Raman Spectroscopy", description, "raman_spectrometer.png", "char_images")

def open_ellipsometry_analysis():
    description = """ELLIPSOMETRY: Thin Film Optical Characterization

Fundamentals:
Measures polarization changes in reflected light to determine thin film properties.

Key Measurements:
• Thickness (sub-nm to μm)
• Refractive index (n and k)
• Optical constants
• Interface quality
• Anisotropy

Technique Variants:
1. Spectroscopic Ellipsometry
2. Imaging Ellipsometry
3. In-situ Ellipsometry
4. Mueller Matrix Ellipsometry

Technical Specifications:
• Wavelength range: 190-1700nm
• Angle range: 45-90°
• Thickness accuracy: <0.1nm
• Measurement speed: ms to s
• Spot size: 10μm to mm

Data Analysis:
• Optical model construction
• Layer-by-layer fitting
• Dispersion relations
• Anisotropy modeling

Applications:
• Semiconductor thin films
• Optical coatings
• Organic layers
• Surface roughness
• Process monitoring"""
    create_tech_window("Ellipsometry", description, "ellipsometer.png", "char_images")

# Main window creation
root = tk.Tk()
root.title("Characterization and Lithography GUI")
root.geometry("600x400")
root.configure(bg='white')

# Center frame to hold the dropdowns and their labels
center_frame = tk.Frame(root, bg='white')
center_frame.place(relx=0.5, rely=0.5, anchor='center')

# Left side - Lithography
left_frame = tk.Frame(center_frame, bg='white')
left_frame.grid(row=0, column=0, padx=20)

# Lithography Process Button
litho_process_btn = ttk.Button(left_frame, text="Process", command=open_litho_process)
litho_process_btn.pack(pady=(0, 10))

left_title_frame = tk.Frame(left_frame, bg='white')
left_title_frame.pack()

lithography_label = tk.Label(left_title_frame, text="Lithography", font=("Arial", 14), bg='white')
lithography_label.pack(side='left')

lithography_info = tk.Label(left_title_frame, text="ℹ️", font=("Arial", 12), bg='white', fg='blue', cursor="hand2")
lithography_info.pack(side='left', padx=5)

lithography_description = """Lithography is a microfabrication process used to pattern thin films and substrates.
It involves using light to transfer a geometric pattern from a photomask to a light-sensitive chemical photoresist.
Common types include optical lithography, electron-beam lithography, and nanoimprint lithography."""
CreateToolTip(lithography_info, lithography_description)

options1 = ["Optical Lithography", "Electron-beam Lithography", 
            "Nanoimprint Lithography", "X-ray Lithography", "UV Lithography"]
selected_option1 = tk.StringVar()
dropdown1 = ttk.Combobox(left_frame, textvariable=selected_option1, values=options1, state="readonly", width=25)
dropdown1.pack(pady=10)
dropdown1.bind("<<ComboboxSelected>>", lambda e: open_selected_litho(selected_option1.get()))

# Right side - Characterization
right_frame = tk.Frame(center_frame, bg='white')
right_frame.grid(row=0, column=1, padx=20)

# Characterization Process Button
char_process_btn = ttk.Button(right_frame, text="Process", command=open_char_process)
char_process_btn.pack(pady=(0, 10))

right_title_frame = tk.Frame(right_frame, bg='white')
right_title_frame.pack()

characterization_label = tk.Label(right_title_frame, text="Characterization", font=("Arial", 14), bg='white')
characterization_label.pack(side='left')

characterization_info = tk.Label(right_title_frame, text="ℹ️", font=("Arial", 12), bg='white', fg='blue', cursor="hand2")
characterization_info.pack(side='left', padx=5)

characterization_description = """Characterization refers to the analysis of material properties and structures.
It includes techniques to examine physical, chemical, and structural characteristics at various scales.
Common methods include microscopy, spectroscopy, diffraction, and surface analysis."""
CreateToolTip(characterization_info, characterization_description)

options2 = ["Scanning Electron Microscopy", "Atomic Force Microscopy",
            "X-ray Diffraction", "Raman Spectroscopy", "Ellipsometry"]
selected_option2 = tk.StringVar()
dropdown2 = ttk.Combobox(right_frame, textvariable=selected_option2, values=options2, state="readonly", width=25)
dropdown2.pack(pady=10)
dropdown2.bind("<<ComboboxSelected>>", lambda e: open_selected_char(selected_option2.get()))

# Function to handle lithography technique selection
def open_selected_litho(technique):
    if technique == "Optical Lithography":
        open_optical_litho()
    elif technique == "Electron-beam Lithography":
        open_ebeam_litho()
    elif technique == "Nanoimprint Lithography":
        open_nanoimprint_litho()
    elif technique == "X-ray Lithography":
        open_xray_litho()
    elif technique == "UV Lithography":
        open_uv_litho()

# Function to handle characterization technique selection
def open_selected_char(technique):
    if technique == "Scanning Electron Microscopy":
        open_sem_analysis()
    elif technique == "Atomic Force Microscopy":
        open_afm_analysis()
    elif technique == "X-ray Diffraction":
        open_xrd_analysis()
    elif technique == "Raman Spectroscopy":
        open_raman_analysis()
    elif technique == "Ellipsometry":
        open_ellipsometry_analysis()

# Start the GUI event loop
root.mainloop()