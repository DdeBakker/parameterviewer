from qgis.core import QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
from qgis.PyQt.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont


class MeasurementPointWidget:
    """
    Klasse om HTML template om te zetten naar Python widget voor QGIS
    """
    
    def __init__(self):
        self.widget = None
    
    def create_html_template(self, measurement_point_name, aggregated_data):
        """
        Creëert HTML template string voor gebruik in QGIS
        """
        html_template = f"""
        <div style="max-width: 350px; min-width: 350px; max-height: 200px; 
                    overflow-y: auto; margin-bottom: 10px; padding: 8px; 
                    border: 1px solid #ddd; border-radius: 3px; 
                    background-color: #f9f9f9; font-size: 11px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 5px; 
                       color: #333; position: sticky; top: 0; background-color: #f9f9f9; 
                       border-bottom: 1px solid #ccc; padding-bottom: 2px;">
                {measurement_point_name}
            </div>
            <div style="line-height: 1.3;">
                • {aggregated_data}
            </div>
        </div>
        """
        return html_template
    
    def create_qgis_expression_template(self):
        """
        Creëert de originele QGIS expression als string voor gebruik in templates
        """
        expression_template = '''<div style="max-width: 350px; min-width: 350px; max-height: 200px; overflow-y: auto; margin-bottom: 10px; padding: 8px; border: 1px solid #ddd; border-radius: 3px; background-color: #f9f9f9; font-size: 11px;">
    <div style="font-weight: bold; font-size: 12px; margin-bottom: 5px; color: #333; position: sticky; top: 0; background-color: #f9f9f9; border-bottom: 1px solid #ccc; padding-bottom: 2px;">
        [% "MeasurementPointName" %]
    </div>
    <div style="line-height: 1.3;">
        • [% 
        aggregate(
            @layer,
            'concatenate',
            "ParameterName" || ': ' || "ParameterMeasuredValue" || ' ' || "ParameterUnit" || ' (' || "AnalysisSampleFrom" || '-' || "AnalysisSampleTo" || ')',
            "MeasurementPointName" = attribute(@parent, 'MeasurementPointName'),
            '<br>• ',
            order_by := "ParameterName"
        ) 
        %]
    </div>
</div>'''
        return expression_template
    
    def set_layer_popup_template(self, layer):
        """
        Stelt de popup template in voor een QGIS layer
        """
        if layer and hasattr(layer, 'setMapTipTemplate'):
            template = self.create_qgis_expression_template()
            layer.setMapTipTemplate(template)
            # Enable map tips for this layer
            layer.setMapTipsEnabled(True)
            return True
        return False
    
    def evaluate_expression_manually(self, layer, feature):
        """
        Evalueert de expressie handmatig in Python
        """
        try:
            measurement_point_name = feature["MeasurementPointName"]
            
            # Verzamel alle features met hetzelfde MeasurementPointName
            matching_features = []
            for f in layer.getFeatures():
                if f["MeasurementPointName"] == measurement_point_name:
                    matching_features.append(f)
            
            # Sorteer op ParameterName
            matching_features.sort(key=lambda x: x["ParameterName"] if x["ParameterName"] else "")
            
            # Bouw de geaggregeerde string
            parameter_strings = []
            for f in matching_features:
                param_string = (
                    f"{f['ParameterName']}: "
                    f"{f['ParameterMeasuredValue']} "
                    f"{f['ParameterUnit']} "
                    f"({f['AnalysisSampleFrom']}-{f['AnalysisSampleTo']})"
                )
                parameter_strings.append(param_string)
            
            aggregated_data = "<br>• ".join(parameter_strings)
            
            return self.create_html_template(measurement_point_name, aggregated_data)
        
        except Exception as e:
            return f"<div>Error processing feature: {str(e)}</div>"