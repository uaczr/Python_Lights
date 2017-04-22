/* 
 * Copyright (C) 2006-2013  Music Technology Group - Universitat Pompeu Fabra
 *
 * This file is part of Gaia
 * 
 * Gaia is free software: you can redistribute it and/or modify it under 
 * the terms of the GNU Affero General Public License as published by the Free 
 * Software Foundation (FSF), either version 3 of the License, or (at your 
 * option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT 
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more 
 * details.
 * 
 * You should have received a copy of the Affero GNU General Public License
 * version 3 along with this program.  If not, see http://www.gnu.org/licenses/
 */

#include "addfield.h"

namespace gaia2 {

AddField::AddField(const ParameterMap& params) : Analyzer(params) {
  validParams = QStringList() << "real" << "string" << "default" << "size";

  _real = params.value("real", QStringList()).toStringList();
  _string = params.value("string", QStringList()).toStringList();
  _default = params.value("default", ParameterMap()).toParameterMap();
  _size = params.value("size", ParameterMap()).toParameterMap();
}


Transformation AddField::analyze(const DataSet* dataset) const {
  G_INFO("Doing addfield analysis...");
  checkDataSet(dataset);

  const PointLayout& layout = dataset->layout();

  // check the fields don't already exist
  QStringList wildcardNames = QStringList(_real) << _string;
  for (int i=0; i<wildcardNames.size(); i++) {
    wildcardNames[i] += ".*";
  }

  QStringList overlap;
  try {
    overlap = layout.descriptorNames(UndefinedType, wildcardNames, false);
  }
  catch (GaiaException&) {
    ; // don't do anything, but overlap is empty
  }

  if (!overlap.isEmpty()) {
    throw GaiaException("The following fields already exist: ", overlap.join(" "));
  }

  // check there are no empty names
  foreach (QString name, _real) {
    if (name == "") throw GaiaException("Name is empty!");
  }
  foreach (QString name, _string) {
    if (name == "") throw GaiaException("Name is empty!");
  }

  // check default values actually correspond to newly created descriptors
  foreach (QString name, _default.keys()) {
    if (!_real.contains(name) && !_string.contains(name)) {
      throw GaiaException("AddField: providing default value for field ",
                          name, ", which isn't supposed to be created");
    }
  }

  // check specified sizes actually correspond to newly created descriptors and are valid
  foreach (QString name, _size.keys()) {
    if (!_real.contains(name) && !_string.contains(name)) {
      throw GaiaException("AddField: providing size for field ",
                          name, ", which isn't supposed to be created");
    }

    bool ok;
    int size = _size.value(name).toInt(&ok);
    if (!ok || (size < 1)) {
      throw GaiaException("AddField: invalid size for field ", name, ": ", _size.value(name));
    }

    if (_default.contains(name) && _default.value(name).toList().size() != size) {
      throw GaiaException("AddField: you gave a default value for field ", name,
                          " which is not of the specified size ", size);
    }
  }

  Transformation result(dataset->layout());
  result.analyzerName = "addfield";
  result.analyzerParams = _params;
  result.applierName = "addfieldapplier";
  result.params = _params;

  return result;
}


} // namespace gaia2
