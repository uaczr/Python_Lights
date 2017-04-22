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

#ifndef GAIA_FROZENLINEARCOMBINATIONDISTANCE_H
#define GAIA_FROZENLINEARCOMBINATIONDISTANCE_H

#include "frozendistance.h"

namespace gaia2 {


class FrozenLinearCombinationDistance : public FrozenDistance {
public:
  FrozenLinearCombinationDistance(const FrozenDataSet& dataset, const ParameterMap& params)
    : FrozenDistance(dataset) {

    validParams << "NO_PARAMS_CHECK";

    if (params.empty()) throw GaiaException("Cannot create a linear combination distance with no params...");

    ParameterMap::const_iterator it = params.constBegin();
    for (; it != params.constEnd(); ++it) {
      ParameterMap dparams = it.value().toParameterMap();
      if (dparams.size() != 3 || !dparams.contains("distance") ||
          !dparams.contains("params") || !dparams.contains("weight")) {
        throw GaiaException("Params map should contain the following keys (and only those): distance, params, weight");
      }

      QString dname = dparams["distance"].toString().toLower();
      ParameterMap params = dparams["params"].toParameterMap();
      FrozenDistance* dist = FrozenMetricFactory::create(dname, dataset, params);

      _dists.push_back(qMakePair((Real)dparams["weight"].toDouble(), dist));
    }
  }

  ~FrozenLinearCombinationDistance() {
    for (uint i=0; i<_dists.size(); i++) delete _dists[i].second;
  }

  void prepare(const FrozenPoint& query) {
    for (uint i=0; i<_dists.size(); i++) {
      _dists[i].second->prepare(query);
    }
  }

  Real operator()(int i, const FrozenPoint& query) const {
    Real result = _dists[0].first * (*_dists[0].second)(i, query);
    for (uint j=1; j<_dists.size(); j++) {
      result += _dists[j].first * (*_dists[j].second)(i, query);
    }
    return result;
  }

protected:
  std::vector<QPair<Real, FrozenDistance*> > _dists;
};



} // namespace gaia2

#endif // GAIA_FROZENLINEARCOMBINATIONDISTANCE_H
