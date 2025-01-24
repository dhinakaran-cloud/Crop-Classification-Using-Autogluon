from flask import Flask, render_template, request
import pandas as pd
import os
from model import predict

app = Flask(__name__)

crop_descriptions = {
    "rice": "Rice is a staple food for more than half of the world’s population, particularly in Asia. It is cultivated in flooded fields known as paddies, which help control weeds and pests. Rice is a rich source of carbohydrates, providing energy and essential nutrients like vitamins and minerals. There are many varieties of rice, including long-grain, medium-grain, and short-grain, each suited to different culinary uses.",
    "maize": "Also known as corn, maize is one of the most widely grown crops in the world. It serves multiple purposes, from human consumption to livestock feed, and is a key ingredient in products like cornmeal, corn syrup, and ethanol. Maize is rich in carbohydrates and also provides dietary fiber and essential nutrients. It is a versatile crop that can be grown in a variety of climates and soil types.",
    "chickpea": "Chickpeas, also known as garbanzo beans, are a nutrient-dense legume high in protein and fiber. They are a staple in Mediterranean and Middle Eastern cuisines, used in dishes such as hummus, falafel, and stews. Chickpeas are also beneficial for soil health as they fix nitrogen, enriching the soil for subsequent crops. They are rich in vitamins and minerals, including folate, iron, and phosphorus.",
    "kidneybeans": "Kidney beans are named for their distinctive kidney shape and are commonly used in chili, soups, and salads. They are a rich source of plant-based protein, fiber, and essential nutrients such as iron and folate. Kidney beans also contain antioxidants that may help reduce the risk of chronic diseases. However, they must be cooked properly, as raw kidney beans contain a toxin that can cause digestive issues.",
    "pigeonpeas": "Pigeon peas are a legume crop that is widely grown in tropical and subtropical regions. They are an important source of protein and amino acids in many developing countries. Pigeon peas are used in a variety of dishes, including Indian dal and Caribbean rice and peas. The plants are drought-resistant and help improve soil fertility through nitrogen fixation.",
    "mothbeans": "Moth beans are a drought-resistant legume cultivated primarily in arid regions. They are valued for their edible seeds, which are high in protein and used in various traditional dishes. Moth beans also serve as fodder for livestock and help improve soil health by fixing nitrogen. They are a resilient crop that can thrive in poor soil conditions and with minimal water.",
    "mungbean": "Mungbeans, also known as green gram, are small, green legumes that are widely used in Asian cuisine. They are rich in protein, fiber, and essential nutrients such as folate and magnesium. Mungbeans are often sprouted and used in salads, stir-fries, and soups. They also play a role in improving soil health by fixing nitrogen and can be grown as a cover crop.",
    "blackgram": "Blackgram, also known as urad dal, is a highly nutritious legume commonly used in Indian cuisine. It is rich in protein, fiber, and essential minerals like potassium, magnesium, and iron. Blackgram is used to make dal, idli, dosa, and various other dishes. The plant also benefits soil health through nitrogen fixation and is often grown in rotation with cereals.",
    "lentil": "Lentils are small, lens-shaped legumes that come in various colors, including green, brown, and red. They are a staple food in many cultures and are known for their high protein and fiber content. Lentils are used in soups, stews, salads, and as a meat substitute in vegetarian dishes. They are also easy to cook and digest, making them a versatile and healthy food choice.",
    "pomegranate": "Pomegranates are known for their juicy, ruby-red seeds called arils, which are packed with antioxidants, vitamins, and minerals. The fruit is valued for its health benefits, including anti-inflammatory properties and potential heart health support. Pomegranates are consumed fresh, juiced, or used in cooking and baking. The plant is well-suited to Mediterranean climates and can be grown in arid conditions.",
    "banana": "Bananas are one of the most popular fruits worldwide, known for their sweet taste and high potassium content. They are a good source of vitamins, including vitamin C and B6, and dietary fiber. Bananas are often eaten fresh but can also be used in baking, cooking, and smoothies. The plant is tropical and thrives in warm, humid climates, making it a major crop in many tropical countries.",
    "mango": "Mangoes are a tropical fruit that are enjoyed for their sweet, juicy flesh and fragrant aroma. They are rich in vitamins A and C, as well as fiber and antioxidants. Mangoes are used in a variety of culinary applications, from fresh eating to smoothies, salads, and desserts. The trees are well-adapted to hot, humid climates and can produce fruit for many years.",
    "grapes": "Grapes are versatile fruits used for fresh consumption, wine production, raisins, and juice. They are rich in antioxidants, particularly resveratrol, which is associated with heart health benefits. Grapes come in various colors, including green, red, and black, and are grown in temperate climates worldwide. The vine plants require careful management and pruning to produce high-quality fruit.",
    "watermelon": "Watermelons are large, refreshing fruits with a high water content, making them a popular choice in hot weather. They are a good source of vitamins A and C and contain antioxidants like lycopene. Watermelons are enjoyed fresh, in salads, or as juice, and their seeds are also edible and nutritious. The plants thrive in warm climates and need ample space to grow their sprawling vines.",
    "muskmelon": "Muskmelons, also known as cantaloupes, are sweet, fragrant melons with orange flesh. They are rich in vitamins A and C, as well as antioxidants and dietary fiber. Muskmelons are often eaten fresh, in fruit salads, or as a refreshing snack. The plants grow best in warm, sunny conditions with well-drained soil.",
    "apple": "Apples are one of the most widely cultivated and consumed fruits globally, known for their crisp texture and sweet-tart flavor. They are rich in dietary fiber, vitamin C, and various antioxidants. Apples come in many varieties, each with its own unique taste and use, from fresh eating to cooking and baking. The trees are temperate and require a cold period to produce fruit.",
    "orange": "Oranges are a citrus fruit valued for their juicy, sweet-tart flavor and high vitamin C content. They are consumed fresh, juiced, or used in cooking and baking. Oranges also provide dietary fiber, folate, and antioxidants. The trees thrive in subtropical and tropical climates and require well-drained soil and plenty of sunlight.",
    "papaya": "Papayas are tropical fruits known for their sweet, orange flesh and numerous health benefits. They are rich in vitamins C and A, as well as digestive enzymes like papain. Papayas are consumed fresh, in smoothies, or used in cooking, especially in Asian cuisine. The plants grow quickly and produce fruit year-round in suitable climates.",
    "coconut": "Coconuts are versatile fruits used for their water, milk, oil, and meat. They are a staple in many tropical diets and provide essential nutrients like potassium, magnesium, and dietary fiber. Coconuts are used in cooking, baking, and beverages, and their oil is widely used in both culinary and cosmetic products. The palm trees are well-adapted to coastal tropical regions.",
    "cotton": "Cotton is a soft, fluffy staple fiber that is spun into yarn and used to make textiles. It is a major cash crop grown in many countries and is essential for the textile industry. Cotton plants require a long frost-free period, plenty of sunshine, and moderate rainfall. The fiber is also used in products like cottonseed oil and animal feed.",
    "jute": "Jute is a long, soft, shiny vegetable fiber that can be spun into coarse, strong threads. It is primarily used to make burlap, hessian, and other packaging materials. Jute plants are grown in tropical regions with high humidity and require well-drained soil. The fiber is also environmentally friendly, being biodegradable and recyclable.",
    "coffee": "Coffee is a brewed drink prepared from roasted coffee beans, which are the seeds of berries from the Coffea plant. It is one of the most popular beverages worldwide and has significant cultural and economic importance. Coffee plants require a tropical climate with rich soil, and the beans go through several processes before becoming the coffee we drink. The beverage is known for its stimulating effects due to caffeine and is enjoyed in various forms, from espresso to cold brew."
}
@app.route('/', methods=['GET'])
def index():
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    return render_template('index.html', features=features)

@app.route('/predict', methods=['POST'])
def predict_crop():
    input_data = {feature: [float(request.form[feature])] for feature in request.form}
    input_df = pd.DataFrame(input_data)
    
   
    prediction = predict(input_df)[0]
    
  
    description = crop_descriptions.get(prediction, "Description not available.")
    
  
    static_dir = os.path.join(app.static_folder)
    jpg_image = f"{prediction}.jpg"
    jpeg_image = f"{prediction}.jpeg"
    
    if jpg_image in os.listdir(static_dir):
        image_file = jpg_image
    elif jpeg_image in os.listdir(static_dir):
        image_file = jpeg_image
    else:
        image_file = "default.jpg"  # Fallback image if neither exists
    
    return render_template('output.html', crop=prediction, description=description, image_file=image_file)

if __name__ == '__main__':
    app.run(debug=True)




# @app.route('/', methods=['GET'])
# def index():
#     features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
#     return render_template('index.html', features=features)

# @app.route('/predict', methods=['POST'])
# def predict_crop():
#     input_data = {feature: [float(request.form[feature])] for feature in request.form}
#     input_df = pd.DataFrame(input_data)
    
#     # Make prediction
#     prediction = predict(input_df)[0]
    
#     # Get the description of the predicted crop
#     description = crop_descriptions.get(prediction, "Description not available.")
    
#     return render_template('output.html', crop=prediction, description=description)

# if __name__ == '__main__':
#     app.run(debug=True)





