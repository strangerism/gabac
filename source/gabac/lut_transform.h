/**
 *  @file lut_transform.h
 */


#ifndef GABAC_LUT_TRANSFORM_H_
#define GABAC_LUT_TRANSFORM_H_

namespace gabac {

class DataBlock;

void transformLutTransform(
        unsigned order,
        DataBlock *transformedSymbols,
        DataBlock *inverseLUT,
        DataBlock *inverseLUT1
);

void inverseTransformLutTransform(
        unsigned order,
        DataBlock *symbols,
        DataBlock *inverseLUT,
        DataBlock *inverseLUT1
);

}  // namespace gabac

// ----------------------------------------------------------------------------

#endif  // GABAC_LUT_TRANSFORM_H_

/* ----------------------------------------------------------------------------
// --------------------------------------------------------------------------*/
