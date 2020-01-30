


<!-- Loading in tensorflow; version at: https://github.com/tensorflow/tfjs -->
<script src = "https://cdn.jsdelivr.net/npm/@tensorflow/rfjs@0.11.2"></script>

const model = await tf.loadLayersModel(' #Insert filepath on webserver here#    model.json'); <!--model.json is given by me-->

<!-- input needs to be formatted as such: [ [Green living area, 1st Floor Square Footage, Total number of rooms above basement] ]

input_initial = tf.tensor(["inputs from user"], [1,3], 'float64'); <!-- [1,3] and 'float64' are constant do not change -->
input = tf.math.log(input_initial);

prediction = model.predict( tf.tensor2d(input)   );
output = tf.math.exp(prediction);