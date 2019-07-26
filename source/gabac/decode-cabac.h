#ifndef GABAC_DECODE_CABAC_H_
#define GABAC_DECODE_CABAC_H_

#include <cstdint>
#include <vector>

namespace gabac {

enum class BinarizationId;
enum class ContextSelectionId;

class DataBlock;

void decode_cabac(const BinarizationId& binarizationId,
                  const std::vector<uint32_t>& binarizationParameters,
                  const ContextSelectionId& contextSelectionId,
                  uint8_t wordsize, DataBlock* bitstream);

}  // namespace gabac

#endif  // GABAC_DECODE_CABAC_H_
