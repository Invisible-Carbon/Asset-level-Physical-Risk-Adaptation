
# Invisible Carbon Climate Risk Assessment Prototype
# Updated with 59 Extreme Heat Days and Property-Specific Heat Amplification

import requests
import pandas as pd
import json
import numpy as np
from datetime import datetime

class ClimateRiskAssessment:
    def __init__(self, api_key, base_url="https://api.riskthinking.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Updated parameters based on RiskThinking.ai 2°C-3°C scenario
        self.extreme_heat_days_2050 = 59  # Updated
        self.extreme_heat_threshold = 35  # Celsius
        self.current_baseline_heat_days = 25

        print(f"🌡️  Climate Assessment initialized:")
        print(f"   • Extreme heat days (2050): {self.extreme_heat_days_2050}")
        print(f"   • Heat threshold: {self.extreme_heat_threshold}°C")
        print(f"   • Baseline increase: {self.extreme_heat_days_2050/self.current_baseline_heat_days:.1f}x")

    def _calculate_updated_heat_risk(self, heat_data, property_type):
        """Calculate heat stress risk score with 59 extreme days and property amplification"""
        if not heat_data:
            heat_data = {
                'current_max_temp': 30,
                '2050_max_temp': 35,
                'extreme_heat_days': self.extreme_heat_days_2050
            }

        future_temp_2050 = heat_data.get('2050_max_temp', 35)

        # Property-specific heat amplification (from user data)
        heat_amplifiers = {
            'Parking Lot': 6,     # +6°C
            'Factory': 4,         # +4°C  
            'Strip Mall': 3,      # +3°C
            'Commercial Building': 2  # +2°C
        }

        heat_island_effect = heat_amplifiers.get(property_type, 2)
        effective_temperature = future_temp_2050 + heat_island_effect

        # Temperature risk: increases above 30°C
        temp_risk = min(100, (effective_temperature - 30) * 7)

        # Extreme days risk: 59 days = maximum risk  
        heat_days_risk = (self.extreme_heat_days_2050 / 59) * 100

        # Amplification factor from baseline increase
        amplification_factor = self.extreme_heat_days_2050 / self.current_baseline_heat_days

        base_heat_risk = (temp_risk * 0.6 + heat_days_risk * 0.4)
        amplified_risk = min(100, base_heat_risk * (1 + (amplification_factor - 1) * 0.5))

        return amplified_risk

    def analyze_sample_properties(self):
        """Analyze sample Scarborough properties without API calls for demo"""

        # Load sample data
        try:
            properties = pd.read_csv('scarborough_sample_properties.csv')
            print(f"\n📍 Loaded {len(properties)} Scarborough properties")
            print(f"📏 Total area: {properties['Square_Footage'].sum():,} sq ft")
        except FileNotFoundError:
            print("❌ scarborough_sample_properties.csv not found")
            return

        results = {}

        print(f"\n🔥 ANALYZING HEAT RISK (59 EXTREME DAYS):")
        print("-" * 60)

        for _, row in properties.iterrows():
            # Simulate climate data
            simulated_climate = {
                '2050_max_temp': 35 + np.random.uniform(0, 3),
                'extreme_heat_days': 59
            }

            heat_risk = self._calculate_updated_heat_risk(simulated_climate, row['Property_Type'])

            # Calculate economic impact
            sq_ft = row['Square_Footage']
            daily_cooling_cost = sq_ft * 0.20
            annual_cooling_cost = daily_cooling_cost * 59

            # Get heat amplification
            amplification = {
                'Parking Lot': '+6°C',
                'Factory': '+4°C', 
                'Strip Mall': '+3°C',
                'Commercial Building': '+2°C'
            }.get(row['Property_Type'], '+2°C')

            results[row['Property_ID']] = {
                'address': row['Address'],
                'type': row['Property_Type'], 
                'sq_ft': sq_ft,
                'heat_amplification': amplification,
                'heat_risk': round(heat_risk, 1),
                'annual_cooling_cost': annual_cooling_cost,
                'cost_per_heat_day': annual_cooling_cost / 59
            }

            print(f"\n🏢 {row['Property_ID']}: {row['Address']}")
            print(f"   Type: {row['Property_Type']} ({sq_ft:,} sq ft)")
            print(f"   Heat Amplification: {amplification}")
            print(f"   Heat Risk Score: {heat_risk:.1f}/100")
            print(f"   Annual Cooling Cost: ${annual_cooling_cost:,.0f}")
            print(f"   Cost per Heat Day: ${annual_cooling_cost/59:,.0f}")

            # Adaptation recommendations
            if row['Property_Type'] == 'Parking Lot':
                print("   🔧 Priority: Permeable surfaces + shade structures")
                print("      Cost: $50,000-$200,000 | Risk reduction: 70-90%")
            elif row['Property_Type'] == 'Factory':
                print("   🔧 Priority: Industrial cooling + ventilation")
                print("      Cost: $75,000-$250,000 | Risk reduction: 70-85%")
            elif row['Property_Type'] == 'Strip Mall':
                print("   🔧 Priority: Cool roof + community cooling center")
                print("      Cost: $15,000-$60,000 | Risk reduction: 60-80%")
            else:
                print("   🔧 Priority: HVAC upgrade + green roof")
                print("      Cost: $40,000-$120,000 | Risk reduction: 65-80%")

        # Summary statistics
        total_cooling_cost = sum(r['annual_cooling_cost'] for r in results.values())
        avg_heat_risk = sum(r['heat_risk'] for r in results.values()) / len(results)

        print(f"\n📊 PORTFOLIO SUMMARY:")
        print(f"   • Total annual cooling costs: ${total_cooling_cost:,.0f}")
        print(f"   • Average heat risk score: {avg_heat_risk:.1f}/100")
        print(f"   • Cost per heat day (portfolio): ${total_cooling_cost/59:,.0f}")
        print(f"   • Properties needing urgent action: {sum(1 for r in results.values() if r['heat_risk'] >= 80)}")

        return results

def main():
    print("🌡️ CLIMATE RISK ASSESSMENT - 59 EXTREME HEAT DAYS")
    print("Property-specific heat amplification:")
    print("• Parking lots: +6°C | Factories: +4°C | Strip malls: +3°C")
    print("=" * 70)

    # For demo purposes, analyze without API
    assessor = ClimateRiskAssessment(api_key="DEMO_MODE")
    results = assessor.analyze_sample_properties()

    print(f"\n✅ Analysis complete! Ready for hackathon demo.")
    print(f"🎯 Key findings:")
    print(f"   • 59 extreme heat days create significant economic burden")
    print(f"   • Property-specific amplification ranges from +2°C to +6°C")
    print(f"   • Adaptation solutions available with 60-90% risk reduction")

if __name__ == "__main__":
    main()
