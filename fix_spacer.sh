#!/bin/bash

echo "🔧 Fixing SpacerComponent error..."

# Backup original file
cp enhanced_m1_m2_m3_integrated_api.py enhanced_m1_m2_m3_integrated_api.py.backup
echo "✅ Backup created"

# Remove SpacerComponent from imports
sed -i '' 's/SpacerComponent,//g' enhanced_m1_m2_m3_integrated_api.py
sed -i '' 's/, SpacerComponent//g' enhanced_m1_m2_m3_integrated_api.py
sed -i '' 's/SpacerComponent//g' enhanced_m1_m2_m3_integrated_api.py
echo "✅ Removed SpacerComponent from imports"

# Replace SpacerComponent usage
sed -i '' 's/SpacerComponent(size="[^"]*")/BoxComponent(layout="vertical", height="12px")/g' enhanced_m1_m2_m3_integrated_api.py
sed -i '' 's/SpacerComponent()/BoxComponent(layout="vertical", height="12px")/g' enhanced_m1_m2_m3_integrated_api.py
echo "✅ Replaced SpacerComponent usage"

echo "🚀 Fix complete! Starting bot..."
python3 enhanced_m1_m2_m3_integrated_api.py