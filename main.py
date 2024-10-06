import gradio as gr
import pandas as pd

df = pd.read_csv('data/exoplanets.csv')

km_per_au = 149597870.7
mass_jupiter_kg = 1.898e27

with gr.Blocks(fill_width=True, fill_height=True, title="ExoView 1.0", ) as demo:
    demo.title = "ExoView 1.0"
    with gr.Column(variant="panel"):
        planet_dropdown = gr.Dropdown(list(df["pl_name"]), label="Exoplanet",
                                      info="Please select exoplanet from dropdown below to Preview")

        with gr.Row(variant="panel", equal_height=True):
            def on_planet_selected(planet_name: str, ):
                planet = df[df["pl_name"] == planet_name]
                planet_url = f'<iframe src="https://eyes.nasa.gov/apps/exo/#/planet/{planet_name.replace(" ", "_")}" width="100%" height="600"></iframe>'
                planet_disc_year = planet["disc_year"].values[0]
                planet_disc_facility = planet["disc_facility"].values[0]
                planet_radius_au = float(planet["pl_orbsmax"].values[0])
                planet_radius_km = float(planet_radius_au * km_per_au)
                planet_radii = f'{planet_radius_au:,.2f} AU / {planet_radius_km:,.2f} km'
                planet_orb_per_day = float(planet["pl_orbper"].values[0])
                planet_orb_per_year = float(planet["pl_orbper"].values[0]) / 365
                planet_orb_pers = f'{planet_orb_per_day:,.2f} days / {planet_orb_per_year:,.2f} years'
                planet_mass_in_mj = float(planet["pl_bmassj"].values[0])
                planet_mass_in_tons = planet_mass_in_mj * (mass_jupiter_kg / 1000)
                planet_masses = f'{planet_mass_in_mj:,.2f} Masses of Jupiter / {planet_mass_in_tons:,.2f} tons'
                planet_nasa_library = f'https://exoplanetarchive.ipac.caltech.edu/overview/{planet_name}'
                planet_nasa_library_button = gr.Button(variant="primary", value="🚀 Open in NASA's library",
                                                       link=planet_nasa_library)
                return [planet_url, planet_disc_year, planet_disc_facility, planet_radii, planet_orb_pers,
                        planet_masses, planet_nasa_library_button]


            planet_preview = gr.HTML("""
                    <div style="width=100%; height: 600px; background-color: gray; display: flex; justify-content: center; align-items: center;">
                        <h2 style="text-align: center;">Please select exoplanet from dropdown on top to Preview</h2>
                    </div>
                    """)

            with gr.Column(variant="panel"):
                planet_disc_year_text = gr.Text(label="Planet's discovery year")
                planet_disc_facility_text = gr.Text(label="Planet's discovery facility")
                planet_radii_text = gr.Text(label="Planet's radius", info=" in AU / km")
                planet_orb_per_text = gr.Text(label="Planet's orbital period", info=" in days/ years")
                planet_masses_text = gr.Text(label="Planet's mass", info=" in Masses of Jupiter / tons")
                open_in_nasa_button = gr.Button("Please select exoplanet from dropdown on top to Preview")
            planet_dropdown.input(on_planet_selected, [planet_dropdown],
                                  [planet_preview, planet_disc_year_text, planet_disc_facility_text, planet_radii_text,
                                   planet_orb_per_text,
                                   planet_masses_text, open_in_nasa_button, ])

demo.launch()
