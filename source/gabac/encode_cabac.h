#ifndef GABAC_ENCODE_CABAC_H_
#define GABAC_ENCODE_CABAC_H_

#include <cstdint>
#include <limits>
#include <vector>

namespace gabac {

enum class ReturnCode;
enum class BinarizationId;
enum class ContextSelectionId;

class DataBlock;

ReturnCode encode_cabac(
        const BinarizationId& binarizationId,
        const std::vector<uint32_t>& binarizationParameters,
        const ContextSelectionId& contextSelectionId,
        DataBlock *symbols,
        size_t maxsize = std::numeric_limits<size_t>::max()
);

}  // namespace gabac

#endif  // GABAC_ENCODE_CABAC_H_
