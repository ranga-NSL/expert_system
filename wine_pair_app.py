from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import pandas as pd

# Create a DataFrame for wine pairing rules
wine_pairing_rules = pd.DataFrame({
    'Dish Type': ['Paneer_Tikka', 'Dal_Makhani', 'Vegetable_Jalfrezi', 'Chole', 
                  'Vegetable_Biryani', 'Samosa', 'Chaat', 'Baingan_Bharta', 'Malai_Kofta'],
    'Wine Color': ['white', 'red', 'white', 'rosé', 'white', 'white', 'rosé', 'red', 'white'],
    'Wine Body': ['medium', 'full', 'off-dry', 'fruity', 'dry', 'crisp', 'fruity', 'light', 'semi-dry'],
    'Wine Flavor': ['smooth', 'spicy', 'aromatic', 'sparkling', 'aromatic', 'refreshing', 'sparkling', 'floral', 'buttery'],
    'Wine Brand': ['Chardonnay', 'Shiraz', 'Riesling', 'Prosecco', 'Sauvignon Blanc', 
                   'Sauvignon Blanc', 'Prosecco', 'Pinot Noir', 'Chardonnay']
})

class WinePairingApp(App):
    def build(self):
        self.title = "Wine Pairing Recommendations"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.instruction_label = Label(text="Select a dish type:")
        layout.add_widget(self.instruction_label)

        self.dish_type_spinner = Spinner(
            text='Select a dish type',
            values=wine_pairing_rules['Dish Type'].tolist()
        )
        layout.add_widget(self.dish_type_spinner)

        self.recommendation_label = Label(text="", size_hint_y=None, height=100)
        layout.add_widget(self.recommendation_label)

        self.recommend_button = Button(text="Get Recommendation", on_press=self.get_wine_recommendation)
        layout.add_widget(self.recommend_button)

        self.exit_button = Button(text="Exit", on_press=self.stop)
        layout.add_widget(self.exit_button)

        return layout

    def get_wine_recommendation(self, instance):
        dish_type = self.dish_type_spinner.text.strip()
        if dish_type == 'Select a dish type':
            self.recommendation_label.text = "Please select a dish type."
            return

        index = wine_pairing_rules[wine_pairing_rules['Dish Type'] == dish_type].index

        if not index.empty:
            wine_info = wine_pairing_rules.loc[index[0]]
            recommendation = (
                f"Suggested wine for {dish_type}: "
                f"Color: {wine_info['Wine Color']}, "
                f"Body: {wine_info['Wine Body']}, "
                f"Flavor: {wine_info['Wine Flavor']}, "
                f"Brand: {wine_info['Wine Brand']}"
            )
            self.recommendation_label.text = recommendation
        else:
            self.recommendation_label.text = f"No wine pairing rule found for {dish_type}."

if __name__ == '__main__':
    WinePairingApp().run()