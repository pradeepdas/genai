import random
import datetime

def generate_apple_health_data(conditions, num_records):
    xml_data = '<HealthData>\n'
    date = datetime.datetime(2024, 1, 1)
    
    condition_count = len(conditions)
    records_per_condition = num_records // condition_count
    
    for condition in conditions:
        for _ in range(records_per_condition):
            date_str = date.isoformat() + 'Z'
            
            if condition == "normal":
                systolic = random.randint(110, 120)
                diastolic = random.randint(70, 80)
                glucose = random.randint(80, 100)
                weight = round(random.uniform(60, 80), 1)
                heart_rate = random.randint(60, 100)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            elif condition == "hypertension":
                systolic = random.randint(130, 150)
                diastolic = random.randint(80, 100)
                glucose = random.randint(100, 120)
                weight = round(random.uniform(80, 100), 1)
                heart_rate = random.randint(70, 110)
                respiratory_rate = random.randint(15, 25)
                oxygen_saturation = random.uniform(90, 95)
            elif condition == "pre_diabetes":
                systolic = random.randint(110, 130)
                diastolic = random.randint(70, 90)
                glucose = random.randint(100, 125)
                weight = round(random.uniform(70, 90), 1)
                heart_rate = random.randint(60, 100)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            elif condition == "obesity":
                systolic = random.randint(110, 130)
                diastolic = random.randint(70, 90)
                glucose = random.randint(80, 100)
                weight = round(random.uniform(100, 130), 1)
                heart_rate = random.randint(60, 100)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            elif condition == "hypotension":
                systolic = random.randint(90, 100)
                diastolic = random.randint(60, 70)
                glucose = random.randint(80, 100)
                weight = round(random.uniform(60, 80), 1)
                heart_rate = random.randint(60, 100)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            elif condition == "bradycardia":
                systolic = random.randint(110, 120)
                diastolic = random.randint(70, 80)
                glucose = random.randint(80, 100)
                weight = round(random.uniform(60, 80), 1)
                heart_rate = random.randint(40, 60)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            elif condition == "tachycardia":
                systolic = random.randint(110, 120)
                diastolic = random.randint(70, 80)
                glucose = random.randint(80, 100)
                weight = round(random.uniform(60, 80), 1)
                heart_rate = random.randint(100, 140)
                respiratory_rate = random.randint(12, 20)
                oxygen_saturation = random.uniform(95, 100)
            
            xml_data += f'''
    <Record type="HKQuantityTypeIdentifierBloodPressureSystolic" sourceName="Health" sourceVersion="14.0" unit="mmHg" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{systolic}"/>
    <Record type="HKQuantityTypeIdentifierBloodPressureDiastolic" sourceName="Health" sourceVersion="14.0" unit="mmHg" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{diastolic}"/>
    <Record type="HKQuantityTypeIdentifierBloodGlucose" sourceName="Health" sourceVersion="14.0" unit="mg/dL" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{glucose}"/>
    <Record type="HKQuantityTypeIdentifierBodyMass" sourceName="Health" sourceVersion="14.0" unit="kg" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{weight}"/>
    <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Health" sourceVersion="14.0" unit="count/min" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{heart_rate}"/>
    <Record type="HKQuantityTypeIdentifierRespiratoryRate" sourceName="Health" sourceVersion="14.0" unit="count/min" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{respiratory_rate}"/>
    <Record type="HKQuantityTypeIdentifierOxygenSaturation" sourceName="Health" sourceVersion="14.0" unit="%" creationDate="{date_str}" startDate="{date_str}" endDate="{date_str}" value="{oxygen_saturation:.2f}"/>
            '''
            
            date += datetime.timedelta(days=1)

    xml_data += '</HealthData>'
    return xml_data

# Example of generating data for different conditions
conditions = ["normal", "hypertension", "pre_diabetes", "obesity", "hypotension", "bradycardia", "tachycardia"]
num_records = 100
health_data = generate_apple_health_data(conditions, num_records)

# Print sample data for verification
print(health_data)
