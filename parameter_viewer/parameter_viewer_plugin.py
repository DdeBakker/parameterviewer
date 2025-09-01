import os
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon, QColor, QFont
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QDialog, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QHBoxLayout, QLabel, QLineEdit, QGroupBox
from qgis.core import QgsProject, QgsVectorLayer, QgsField, QgsFeature, QgsSymbol, QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling
from qgis.core import QgsTextFormat, QgsTextBufferSettings

class BodemkwaliteitNormen:
    """
    Klasse met bodemkwaliteitsnormen uit Bijlage B Regeling bodemkwaliteit 2022
    """
    
    def __init__(self):
        # Kwaliteitseisen - uitgebreid met alle klassen (mg/kg droge stof)
        self.normen = {
            'Arseen': {'Landbouw/Natuur': 20, 'Wonen': 27, 'Industrie': 76, 'Matig Verontreinigd': 76, 'Sterk Verontreinigd': 76},
            'Cadmium': {'Landbouw/Natuur': 0.6, 'Wonen': 1.2, 'Industrie': 4.3, 'Matig Verontreinigd': 13, 'Sterk Verontreinigd': 13},
            'Chroom': {'Landbouw/Natuur': 55, 'Wonen': 62, 'Industrie': 180, 'Matig Verontreinigd': 180, 'Sterk Verontreinigd': 180},
            'Koper': {'Landbouw/Natuur': 40, 'Wonen': 54, 'Industrie': 190, 'Matig Verontreinigd': 190, 'Sterk Verontreinigd': 190},
            'Kwik': {'Landbouw/Natuur': 0.15, 'Wonen': 0.83, 'Industrie': 4.8, 'Matig Verontreinigd': 36, 'Sterk Verontreinigd': 36},
            'Lood': {'Landbouw/Natuur': 50, 'Wonen': 210, 'Industrie': 530, 'Matig Verontreinigd': 530, 'Sterk Verontreinigd': 530},
            'Nikkel': {'Landbouw/Natuur': 35, 'Wonen': 39, 'Industrie': 100, 'Matig Verontreinigd': 100, 'Sterk Verontreinigd': 100},
            'Zink': {'Landbouw/Natuur': 140, 'Wonen': 200, 'Industrie': 720, 'Matig Verontreinigd': 720, 'Sterk Verontreinigd': 720},
            'Benzeen': {'Landbouw/Natuur': 0.2, 'Wonen': 0.2, 'Industrie': 1, 'Matig Verontreinigd': 1.1, 'Sterk Verontreinigd': 1.1},
            'Tolueen': {'Landbouw/Natuur': 0.2, 'Wonen': 0.2, 'Industrie': 1.25, 'Matig Verontreinigd': 32, 'Sterk Verontreinigd': 32},
            'Ethylbenzeen': {'Landbouw/Natuur': 0.2, 'Wonen': 0.2, 'Industrie': 1.25, 'Matig Verontreinigd': 110, 'Sterk Verontreinigd': 110},
            'Xylenen': {'Landbouw/Natuur': 0.45, 'Wonen': 0.45, 'Industrie': 1.25, 'Matig Verontreinigd': 17, 'Sterk Verontreinigd': 17},
            'Naftaleen': {'Landbouw/Natuur': 1, 'Wonen': 1, 'Industrie': 1, 'Matig Verontreinigd': 1, 'Sterk Verontreinigd': 1},
            'Fenol': {'Landbouw/Natuur': 0.25, 'Wonen': 0,25, 'Industrie': 1,25, 'Matig Verontreinigd': 14, 'Sterk Verontreinigd': 14},
            'PAK (som 10)': {'Landbouw/Natuur': 1.5, 'Wonen': 6.8, 'Industrie': 40, 'Matig Verontreinigd': 40, 'Sterk Verontreinigd': 40},
            'Benzo(a)pyreen': {'Landbouw/Natuur': 1, 'Wonen': 1.0, 'Industrie': 1.0, 'Matig Verontreinigd': 1, 'Sterk Verontreinigd': 1},
            'PCB (som 7)': {'Landbouw/Natuur': 0.02, 'Wonen': 0.040, 'Industrie': 0.5, 'Matig Verontreinigd': 1, 'Sterk Verontreinigd': 1},
            'Tetrachlooretheen': {'Landbouw/Natuur': 0.15, 'Wonen': 0.15, 'Industrie': 4, 'Matig Verontreinigd': 8.8, 'Sterk Verontreinigd': 8.8},
            'Trichlooretheen': {'Landbouw/Natuur': 0.25, 'Wonen': 0.15, 'Industrie': 4, 'Matig Verontreinigd': 8.8, 'Sterk Verontreinigd': 8.8},
            'Minerale olie': {'Landbouw/Natuur': 190, 'Wonen': 190, 'Industrie': 500, 'Matig Verontreinigd': 5000, 'Sterk Verontreinigd': 5000},
            'Asbest': {'Landbouw/Natuur': 0, 'Wonen': 100, 'Industrie': 100, 'Matig Verontreinigd': 100, 'Sterk Verontreinigd': 100},
            'Kobalt': {'Landbouw/Natuur': 15, 'Wonen': 35, 'Industrie': 190, 'Matig Verontreinigd': 190, 'Sterk Verontreinigd': 190},
            'Cyanide (vrij)': {'Landbouw/Natuur': 3.0, 'Wonen': 3.0, 'Industrie': 20, 'Matig Verontreinigd': 20, 'Sterk Verontreinigd': 20},
            'Cyanide (complex, pH onbelangrijk)': {'Landbouw/Natuur': 5.5, 'Wonen': 5.5, 'Industrie': 50, 'Matig Verontreinigd': 50, 'Sterk Verontreinigd': 50},
        }
        self.parameter_aliases = {
            'As': 'Arseen','Cd': 'Cadmium','Cr': 'Chroom','Cu': 'Koper','Hg': 'Kwik','Pb': 'Lood',
            'Ni': 'Nikkel','Zn': 'Zink','BTEX': 'Benzeen','PAK': 'PAK (som 10)','PCB': 'PCB (som 7)',
            'Per': 'Tetrachlooretheen','Tri': 'Trichlooretheen','MO': 'Minerale olie','Co': 'Kobalt',
            'Minerale olie': 'Minerale olie (totaal)',
            'Benzeen': 'BTEX', 'PAK (som 10)': 'PAK', 'PCB (som 7)': 'PCB',
            'minerale olie c12-c22': 'Minerale olie',
            'minerale olie c22-c30': 'Minerale olie',
            'minerale olie c30-c40': 'Minerale olie'
        }
        
        # Interventiewaardes voor T130
        self.interventiewaardes_t130 = {
            'Cyanide (complex, pH onbelangrijk)': 50, 'Cyanide (vrij)': 20, 'Thiocyanaten (som)': 20,
            'Benzeen': 1.1, 'Cresolen (som)': 13, 'Ethylbenzeen': 110, 'Fenol': 14, 'Styreen (Vinylbenzeen)': 86,
            'Tolueen': 32, 'Xylenen (som)': 17, '4-Chloor-2-methylfenoxy-azijnzuur': 4, 'Aldrin': 0.32,
            'alfa-Endosulfan': 4, 'alfa-HCH': 17, 'Atrazine': 0.71, 'beta-HCH': 1.6, 'Carbaryl': 0.45,
            'Carbofuran': 0.017, 'Chloordaan (cis + trans)': 4, 'DDD (som)': 34, 'DDE (som)': 2.3,
            'DDT (som)': 34, 'Drins (Aldrin+Dieldrin+Endrin)': 4, 'gamma-HCH': 1.2, 'Heptachloor': 4,
            'Heptachloorepoxide': 4, 'Organotin, som TBT+TFT, als SN': 2.5, '1,1,1-Trichloorethaan': 15,
            '1,1,2-Trichloorethaan': 10, '1,1-Dichloorethaan': 15, '1,1-Dichlooretheen': 0.3,
            '1,2-Dichloorethaan': 6.4, 'Chloornaftaleen': 23, 'cis + trans-1,2-Dichlooretheen': 1,
            'Dichloorbenzenen (som)': 19, 'Dichloorfenolen (som)': 22, 'Dichloormethaan': 3.9,
            'Dichloorpropaan': 2, 'Hexachloorbenzeen (HCB)': 2, 'Monochlooranilinen (som)': 50,
            'Monochloorbenzeen': 7, 'Monochloorfenolen (som)': 5.4, 'PCB (som 7)': 1,
            'Pentachloorbenzeen (QCB)': 6.7, 'Pentachloorfenol (PCP)': 12,
            'Som 29 dioxines (als TEQ)': 0.00018, 'Tetrachloorbenzenen (som)': 11, 'Tetrachlooretheen (Per)': 8.8,
            'Tetrachloorfenolen (som)': 21, 'Tetrachloormethaan (Tetra)': 0.7,
            'Tribroommethaan (bromoform)': 75, 'Trichloorbenzenen (som)': 11, 'Trichlooretheen (Tri)': 2.5,
            'Trichloorfenolen (som)': 22, 'Trichloormethaan (Chloroform)': 5.6, 'Vinylchloride': 0.1,
            'Antimoon': 22, 'Arseen': 76, 'Cadmium': 13, 'Chroom (VI)': 78, 'Chroom': 180, 'Kobalt': 190,
            'Koper': 190, 'Kwik': 36, 'Lood': 530, 'Molybdeen': 190, 'Nikkel': 100, 'Zink': 720,
            'Benzylbutylftalaat': 48, 'Dihexylftalaat': 220, 'methylkwik': 4, 'som gewogen asbest': 100,
            'Bis(ethylhexyl)ftalaat': 60, 'Cyclohexanon': 150, 'Dibutylftalaat': 36, 'Diethylftalaat': 53,
            'Di-isobutylftalaat': 17, 'Dimethylftalaat': 82, 'Minerale olie (totaal)': 5000,
            'Pyridine': 11, 'Tetrahydrofuraan': 7, 'Tetrahydrothiofeen': 8.8, 'PAK (som 10)': 40
        }
    
    def get_kwaliteitsklasse(self, parameter_name, waarde):
        try:
            waarde = float(waarde)
            norm_param = self.parameter_aliases.get(parameter_name, parameter_name)
            if norm_param not in self.normen:
                for param in self.normen.keys():
                    if parameter_name.lower() in param.lower() or param.lower() in parameter_name.lower():
                        norm_param = param; break
            if norm_param not in self.normen:
                return 'Geen Norm','#999999',f"Deze stof heeft geen norm opzichzelf deze wordt gebruik ten calculatie van of PCB's (Som 7) of PAK's (Som 10)"
            normen = self.normen[norm_param]
            if waarde <= normen['Landbouw/Natuur']:
                return 'Landbouw/Natuur','#00aa00',f'≤ {normen["Landbouw/Natuur"]}'
            elif waarde <= normen['Wonen']:
                return 'Wonen','#ffdd00',f'≤ {normen["Wonen"]}'
            elif waarde <= normen['Industrie']:
                return 'Industrie','#ff8800',f'≤ {normen["Industrie"]}'
            elif waarde <= normen['Matig Verontreinigd']:
                return 'Matig Verontreinigd','#ff0000',f'≤ {normen["Matig Verontreinigd"]}'
            else: # Alles wat boven Matig Verontreinigd zit, is Sterk Verontreinigd
                return 'Sterk Verontreinigd','#6600cc',f'> {normen["Matig Verontreinigd"]}'
        except Exception as e:
            return 'Fout','#ff0000',f'Fout: {str(e)}'


class MeasurementPointWidget:
    def __init__(self, parent=None):
        self.widget=None; self.bodem_normen=BodemkwaliteitNormen()


class ParameterViewer:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = '&Parameter Viewer'
        self.measurement_widget = MeasurementPointWidget()
        
        # De variabele is buiten de functieaanroep gedefinieerd om de syntaxfout te herstellen
        icon_path = os.path.join(self.plugin_dir, 'icons', 'icoon.png')
        
        self.add_action(
            icon_path,
            text='Show Parameter Classifications',
            callback=self.show_classifications,
            parent=self.iface.mainWindow())
            
    def initGui(self):
        """Adds plugin actions to the main QGIS menu."""
        # Actions are already added in __init__
        pass

    def add_action(self, icon_path, text, callback, parent):
        """Helper function to add a menu item and a toolbar icon."""
        action = QAction(QIcon(icon_path), text, parent)
        action.triggered.connect(callback)
        self.iface.addPluginToMenu(self.menu, action)
        self.iface.addToolBarIcon(action)
        self.actions.append(action)
        return action

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)

    # Placeholder methods for the menu actions
    def run_simple(self):
        QMessageBox.information(self.iface.mainWindow(), "Info", "Simple template not implemented.")

    def run_complex(self):
        QMessageBox.information(self.iface.mainWindow(), "Info", "Complex template not implemented.")

    def run_classification(self):
        QMessageBox.information(self.iface.mainWindow(), "Info", "Classification template not implemented.")
        
    def run_debug(self):
        QMessageBox.information(self.iface.mainWindow(), "Info", "Debug template not implemented.")

    def show_classifications(self):
        try:
            layer=self.iface.activeLayer()
            if not layer or not isinstance(layer,QgsVectorLayer):
                QMessageBox.warning(self.iface.mainWindow(),"Warning","Please select a vector layer first!"); return
            
            # Bepaal het rapportkopje en de laagtype op basis van de laagnaam
            report_title = "BODEMKWALITEITSCLASSIFICATIE RAPPORT"
            is_t130_layer = False
            layer_name = layer.name()
            
            if "T101" in layer_name:
                report_title = "Rapport Bodemkwaliteit: T101"
            elif "T130" in layer_name:
                report_title = "Rapport Bodemkwaliteit: T130"
                is_t130_layer = True

            # Voeg 'AnalysisSampleName' toe aan de lijst van vereiste velden
            required=['MeasurementPointName','ParameterName','ParameterMeasuredValue','JarFrom','JarTo', 'AnalysisSampleName']
            field_names=[f.name() for f in layer.fields()]
            missing=[f for f in required if f not in field_names]
            
            # Aangepaste controle op ontbrekende velden met de nieuwe pop-up melding
            if 'ParameterName' in missing or 'ParameterMeasuredValue' in missing:
                QMessageBox.warning(self.iface.mainWindow(),"Warning","Deze laag bevat geen gegevens die door deze plugin kunnen worden gebruikt. Controleer of u de juiste laag hebt geselecteerd."); return
            elif missing:
                QMessageBox.warning(self.iface.mainWindow(),"Missing Fields",f"Missing: {', '.join(missing)}"); return
            
            # Lijst van PAK-stoffen die moeten worden uitgesloten van de rapportage
            pak_substances_to_exclude = {
                'naftaleen', 'fenantreen', 'antraceen', 'fluorantheen', 'chryseen', 
                'benzo(a)antraceen', 'benzo(a)pyreen', 'benzo(k)fluorantheen', 
                'indeno(1,2,3cd)pyreen', 'benzo(ghi)peryleen'
            }

            # Aangepaste lijst van stoffen met 'zorgplicht van toepassing'
            # DE FOUT IS HERSTELD MET DE JUISTE EXACTE SNTAX
            zorgplicht_substances = {
                'Barium', 'Droge stof', 'Minerale olie C12 - C22', 'Minerale olie C22 - C30', 'Minerale olie C30 - C40'
            }
            
            # Lijst van parameters die een eigen klasse 'Fysische Parameter' krijgen
            physical_substances = {
                'organische stof (humus)', 'lutum'
            }

            # Lijst van stoffen die deel uitmaken van een somparameter en een specifieke beschrijving moeten krijgen
            som_parameters_for_description = {
                'fenantreen', 'antraceen', 'fluorantheen', 'chryseen',
                'benzo(a)antraceen', 'benzo(k)fluorantheen',
                'indeno(1,2,3cd)pyreen', 'benzo(ghi)peryleen', 'naftaleen',
                'p,p-ddd', 'p,p-dde', 'p,p-ddt'
            }
            
            # Definieer de hiërarchie van klassen met numerieke prioriteit
            # Hogere waarde = hogere prioriteit
            class_priority = {
                'Onbekend': 0,
                'Fysische Parameter': 1,
                'Geen Norm': 2,
                'Zorgplicht': 3,
                'Landbouw/Natuur': 4,
                'Kleiner dan gelijk aan interventiewaarde': 5,
                'Wonen': 6,
                'Industrie': 7,
                'Matig Verontreinigd': 8,
                'Sterk Verontreinigd': 9,
                'Groter dan interventiewaarde': 10
            }
            
            # Aangepast naar een lijst om alle features te behouden, zelfs met identieke meetpunt-parameter combinaties
            classifications = []
            field_indices = {f.name(): i for i, f in enumerate(layer.fields())}
            
            # Groepeer features per meetpunt
            grouped_features = {}
            for feat in layer.getFeatures():
                mp = feat.attributes()[field_indices["MeasurementPointName"]] if "MeasurementPointName" in field_indices else "Unknown"
                if mp not in grouped_features:
                    grouped_features[mp] = {'features': [], 'geometry': feat.geometry()}
                grouped_features[mp]['features'].append(feat)

            # --- START: New logic for layer visualization ---
            crs = layer.crs().authid()
            classified_layer = QgsVectorLayer(f"Point?crs={crs}", "Bodemkwaliteit Klassificatie", "memory")
            if not classified_layer.isValid():
                QMessageBox.critical(self.iface.mainWindow(), "Fout", "Kon geen nieuwe laag creëren.")
                return

            classified_layer_provider = classified_layer.dataProvider()
            # Add both Classification and MeasurementPointName fields
            classified_layer_provider.addAttributes([QgsField("Classification", QVariant.String), QgsField("MeasurementPointName", QVariant.String)])
            classified_layer.updateFields()

            classified_features = []
            
            for mp, data in grouped_features.items():
                highest_class = 'Onbekend'
                
                # Bepaal de hoogste klasse voor het meetpunt
                for feat in data['features']:
                    pn = feat.attributes()[field_indices["ParameterName"]] if "ParameterName" in field_indices else "Unknown"
                    val = feat.attributes()[field_indices["ParameterMeasuredValue"]] if "ParameterMeasuredValue" in field_indices else None
                    unit = feat.attributes()[field_indices["ParameterUnit"]] if "ParameterUnit" in field_indices else ""
                    jar_from = feat.attributes()[field_indices["JarFrom"]] if "JarFrom" in field_indices else "Onbekend"
                    jar_to = feat.attributes()[field_indices["JarTo"]] if "JarTo" in field_indices else "Onbekend"
                    asn = feat.attributes()[field_indices["AnalysisSampleName"]] if "AnalysisSampleName" in field_indices else "Onbekend"
                    
                    if pn.lower().strip() in pak_substances_to_exclude:
                        continue
                    
                    current_class = "Onbekend"
                    toel = ""
                    
                    if pn.lower().strip() in physical_substances:
                        if val is not None:
                            current_class = 'Fysische Parameter'
                            toel = 'Fysische parameter zonder normwaarde'
                    elif pn.strip() in zorgplicht_substances:
                        if val is not None:
                            current_class = 'Zorgplicht'
                            toel = 'Zorgplicht van toepassing: zowel bij ontbrekende normwaarde als bij ontbrekend IW.'
                    elif val is not None:
                        if pn.lower().strip() in som_parameters_for_description:
                            current_class = 'Geen Norm'
                            toel = "Deze stof heeft geen norm opzichzelf deze wordt gebruik ten calculatie van of PCB's (Som 7) of PAK's (Som 10)"
                        elif is_t130_layer:
                            norm_param_t130 = self.measurement_widget.bodem_normen.parameter_aliases.get(pn, pn)
                            if norm_param_t130 in self.measurement_widget.bodem_normen.interventiewaardes_t130:
                                interventiewaarde = self.measurement_widget.bodem_normen.interventiewaardes_t130[norm_param_t130]
                                if float(val) > float(interventiewaarde):
                                    current_class = 'Groter dan interventiewaarde'
                                    toel = f'De waarde ({val}) is groter dan de interventiewaarde van {interventiewaarde}.'
                                else:
                                    current_class = 'Kleiner dan gelijk aan interventiewaarde'
                                    toel = f'De waarde ({val}) is kleiner dan of gelijk aan de interventiewaarde van {interventiewaarde}.'
                            else:
                                current_class = 'Geen Norm'
                                toel = 'Deze parameter heeft geen interventiewaarde.'
                        else:
                            current_class, _, toel = self.measurement_widget.bodem_normen.get_kwaliteitsklasse(pn, val)
                    
                    # Vergelijk de huidige klasse met de hoogste klasse tot nu toe
                    if class_priority.get(current_class, 0) > class_priority.get(highest_class, 0):
                        highest_class = current_class
                    
                    classifications.append({
                        'measurement_point': mp,
                        'analysis_sample_name': asn,
                        'parameter': pn,
                        'value': val,
                        'unit': unit,
                        'class': current_class,
                        'description': toel,
                        'jar_from': jar_from,
                        'jar_to': jar_to
                    })
                
                # Voeg nu één feature toe per meetpunt met de hoogste klasse, tenzij het een 'niet-relevante' klasse is.
                if highest_class not in ['Onbekend', 'Fysische Parameter', 'Geen Norm']:
                    new_feature = QgsFeature()
                    new_feature.setGeometry(data['geometry'])
                    new_feature.setAttributes([highest_class, mp])
                    classified_features.append(new_feature)

            if not classifications:
                QMessageBox.warning(self.iface.mainWindow(),"No Data","No parameter data found"); return

            if not classified_features:
                QMessageBox.warning(self.iface.mainWindow(), "Geen gegevens", "Geen parametergegevens gevonden voor classificatie.")
                return

            classified_layer_provider.addFeatures(classified_features)

            target_field = "Classification"
            # Define all possible categories to ensure a consistent legend
            if is_t130_layer:
                all_possible_classes = ['Kleiner dan gelijk aan interventiewaarde', 'Groter dan interventiewaarde', 'Zorgplicht']
            else:
                all_possible_classes = ['Landbouw/Natuur', 'Wonen', 'Industrie', 'Matig Verontreinigd', 'Sterk Verontreinigd', 'Zorgplicht']

            # Add other classes to show their legends regardless of whether they are present in the data
            all_possible_classes.extend(['Fysische Parameter', 'Geen Norm'])
            
            color_map = {
                'Landbouw/Natuur': '#00aa00',
                'Wonen': '#ffdd00',
                'Industrie': '#ff8800',
                'Matig Verontreinigd': '#ff0000',
                'Sterk Verontreinigd': '#6600cc',
                'Groter dan interventiewaarde': '#ff0000',
                'Kleiner dan gelijk aan interventiewaarde': '#00aa00',
                'Zorgplicht': '#0000ff',
                'Fysische Parameter': '#999999',
                'Geen Norm': '#000000',
                'Onbekend': '#999999'
            }

            renderer = QgsCategorizedSymbolRenderer(target_field)
            
            # Loop through the list of all possible classes to create the symbology
            for class_name in all_possible_classes:
                color = color_map.get(class_name, '#999999')
                symbol = QgsSymbol.defaultSymbol(classified_layer.geometryType())
                symbol.setColor(QColor(color))
                category = QgsRendererCategory(class_name, symbol, class_name)
                renderer.addCategory(category)
            
            classified_layer.setRenderer(renderer)
            
            # --- START: Labeling Configuration ---
            label_settings = QgsPalLayerSettings()
            label_settings.enabled = True
            label_settings.fieldName = "MeasurementPointName"
            
            text_format = QgsTextFormat()
            font = QFont()
            font.setPointSize(8)
            font.setBold(True)
            text_format.setFont(font)
            text_format.setColor(QColor("black"))
            
            # Optional: Add a text buffer (halo) for better readability
            buffer_settings = QgsTextBufferSettings()
            buffer_settings.setEnabled(True)
            buffer_settings.setColor(QColor("white"))
            buffer_settings.setSize(1.0)
            text_format.setBuffer(buffer_settings)
            
            label_settings.setFormat(text_format)
            
            # Create a labeling object and apply the settings
            labeling = QgsVectorLayerSimpleLabeling(label_settings)
            classified_layer.setLabeling(labeling)
            classified_layer.setLabelsEnabled(True)
            
            # --- END: Labeling Configuration ---
            
            QgsProject.instance().addMapLayer(classified_layer)
            self.iface.zoomToActiveLayer()
            QMessageBox.information(self.iface.mainWindow(), "Succes", "Geklassificeerde laag is aan de kaart toegevoegd.")

            # Bijgewerkte kleurenmap met rood/witte symbolen
            kleuren_map={'Landbouw/Natuur':'🟢','Wonen':'🟡','Industrie':'🟠','Matig Verontreinigd':'🔴','Sterk Verontreinigd':'🟣',
                         'Zorgplicht':'🔵', 'Fysische Parameter':'⚪', 'Geen Norm':'⚫', 
                         'Groter dan interventiewaarde': '🔴', 'Kleiner dan gelijk aan interventiewaarde': '🟢', 'Onbekend':'?', 'Error':'⚠️'}
            
            # Create the dialog with filter and sort options
            dlg=QDialog(self.iface.mainWindow()); dlg.setWindowTitle("Parameter Classifications")
            layout=QVBoxLayout(dlg)
            
            # Hoofdstyling voor het venster en de widgets
            dialog_style = """
                QDialog {
                    background-color: white;
                }
                QGroupBox {
                    border: 1px solid #808080;
                    border-radius: 5px;
                    margin-top: 2ex;
                    background-color: #F8F8F8;
                    color: #808080;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 3px;
                }
                QLabel {
                    color: black;
                }
                QPushButton {
                    background-color: #808080;
                    color: white;
                    border: 1px solid #808080;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #A0A0A0;
                }
                QComboBox {
                    background-color: white;
                    color: black;
                    border: 1px solid #808080;
                    border-radius: 5px;
                    padding: 2px;
                    padding-right: 20px; /* Ruimte voor de dropdown-pijl */
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;
                    border-left-width: 1px;
                    border-left-color: darkgray;
                    border-left-style: solid; /* Zorgt voor een scheidingslijn */
                    border-top-right-radius: 5px;
                    border-bottom-right-radius: 5px;
                }
                QComboBox::down-arrow {
                    image: url("C:/path/to/red_arrow.png"); /* Optioneel: vervang met een rode pijl-afbeelding */
                    background-color: #808080;
                    width: 10px;
                    height: 10px;
                }
                QLineEdit, QTextEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #808080;
                    border-radius: 5px;
                    padding: 2px;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f0f0f0;
                    width: 10px;
                }
                QScrollBar::handle:vertical {
                    background: #808080;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                    border: none;
                    width: 0px;
                    height: 0px;
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """
            dlg.setStyleSheet(dialog_style)

            # --- Groepering van de opties in een QGroupBox ---
            options_groupbox = QGroupBox("Rapportage Opties")
            options_layout = QVBoxLayout()

            # Filter functionality
            filter_layout = QHBoxLayout()
            filter_label = QLabel("Filter op klasse:")
            filter_combobox = QComboBox()
            if is_t130_layer:
                fixed_class_order = ['Toon alles', 'Kleiner dan gelijk aan interventiewaarde', 'Groter dan interventiewaarde', 'Fysische Parameter', 'Zorgplicht', 'Geen Norm']
            else:
                fixed_class_order = ['Toon alles', 'Landbouw/Natuur', 'Wonen', 'Industrie', 'Matig Verontreinigd', 'Sterk Verontreinigd', 'Fysische Parameter', 'Zorgplicht', 'Geen Norm']
            filter_combobox.addItems(fixed_class_order)
            filter_layout.addWidget(filter_label)
            filter_layout.addWidget(filter_combobox)
            options_layout.addLayout(filter_layout)
            
            # Sorting functionality
            sort_layout = QHBoxLayout()
            sort_label = QLabel("Sorteren op:")
            sort_combobox = QComboBox()
            sort_combobox.addItem("Sorteren op Meetpunt")
            sort_combobox.addItem("Sorteren op Parameter")
            sort_combobox.addItem("Sorteren op Analysenaam")
            sort_layout.addWidget(sort_label)
            sort_layout.addWidget(sort_combobox)
            options_layout.addLayout(sort_layout)

            # Search functionality
            search_layout = QHBoxLayout()
            search_label = QLabel("Zoek op parameter/meetpunt/waarde:")
            search_lineedit = QLineEdit()
            search_lineedit.setPlaceholderText("Bijv. 'Arseen', 'MP01', of '1.5'")
            search_layout.addWidget(search_label)
            search_layout.addWidget(search_lineedit)
            options_layout.addLayout(search_layout)

            options_groupbox.setLayout(options_layout)
            layout.addWidget(options_groupbox)
            
            text=QTextEdit(); text.setReadOnly(True)
            layout.addWidget(text)
            
            def update_report():
                selected_class = filter_combobox.currentText()
                selected_sort = sort_combobox.currentText()
                search_query = search_lineedit.text().lower().strip()
                report=f"{report_title}\n"+"="*50+"\n\n"
                
                filtered_classifications = [
                    info for info in classifications
                    if (selected_class == "Toon alles" or info['class'] == selected_class) and
                    (not search_query or search_query in info['parameter'].lower() or search_query in info['measurement_point'].lower() or search_query in info['analysis_sample_name'].lower() or search_query in str(info['value']).lower())
                ]
                
                if not filtered_classifications:
                    text.setPlainText("Geen resultaten gevonden voor de geselecteerde filter en sorteeropties.")
                    return
                
                if selected_sort == "Sorteren op Parameter":
                    sorted_list = sorted(filtered_classifications, key=lambda x: (x['parameter'], x['measurement_point']))
                    
                    for info in sorted_list:
                        icoon = kleuren_map.get(info['class'], '⚫')
                        report += f"  Meetpunt: {info['measurement_point']}\n"
                        report += f"  Analysenaam: {info['analysis_sample_name']}\n"
                        report += f"  Parameter: {info['parameter']}\n"
                        report += f"    Waarde: {info['value']} {info['unit']}\n"
                        report += f"    Diepte: {info['jar_from']} tot {info['jar_to']} cm\n"
                        report += f"    Klasse: {icoon} {info['class']}\n"
                        report += f"    Details: {info['description']}\n\n"
                elif selected_sort == "Sorteren op Analysenaam":
                    meetpunten = {}
                    for info in filtered_classifications:
                        mp = info['measurement_point']
                        meetpunten.setdefault(mp, []).append(info)

                    for mp in sorted(meetpunten.keys()):
                        report += f"MEETPUNT: {mp}\n" + "-" * 30 + "\n"
                        for info in sorted(meetpunten[mp], key=lambda x: x['analysis_sample_name']):
                            icoon = kleuren_map.get(info['class'], '⚫')
                            report += f"  Analysenaam: {info['analysis_sample_name']}\n"
                            report += f"  Parameter: {info['parameter']}\n"
                            report += f"    Waarde: {info['value']} {info['unit']}\n"
                            report += f"    Diepte: {info['jar_from']} tot {info['jar_to']} cm\n"
                            report += f"    Klasse: {icoon} {info['class']}\n"
                            report += f"    Details: {info['description']}\n\n"
                        report += "\n"
                else: # Sorteren op Meetpunt
                    meetpunten = {}
                    for info in filtered_classifications:
                        mp = info['measurement_point']
                        meetpunten.setdefault(mp, []).append(info)
                    
                    for mp in sorted(meetpunten.keys()):
                        report += f"MEETPUNT: {mp}\n" + "-" * 30 + "\n"
                        for info in sorted(meetpunten[mp], key=lambda x: x['parameter']):
                            icoon = kleuren_map.get(info['class'], '⚫')
                            report += f"  {info['parameter']}:\n"
                            report += f"    Analysenaam: {info['analysis_sample_name']}\n"
                            report += f"    Waarde: {info['value']} {info['unit']}\n"
                            report += f"    Diepte: {info['jar_from']} tot {info['jar_to']} cm\n"
                            report += f"    Klasse: {icoon} {info['class']}\n"
                            report += f"    Details: {info['description']}\n\n"
                        report += "\n"
                
                report+="KWALITEITSKLASSEN LEGENDA:\n"+"-"*30+"\n"
                legend_classes = fixed_class_order[1:]
                for k in legend_classes:
                    if k in kleuren_map:
                         report+=f"{kleuren_map[k]} {k}\n"
                
                text.setPlainText(report)
            
            filter_combobox.currentIndexChanged.connect(update_report)
            sort_combobox.currentIndexChanged.connect(update_report)
            search_lineedit.textChanged.connect(update_report)
            update_report()
            
            btn=QPushButton("Close"); btn.clicked.connect(dlg.accept); layout.addWidget(btn)
            dlg.resize(900,500)
            dlg.setMinimumSize(450, 400) # Voegt minimale grootte toe
            dlg.exec_()

        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(),"Error",f"Error: {str(e)}")
