#ifndef GABAC_RUN_H_
#define GABAC_RUN_H_

namespace gabac {

class EncodingConfiguration;
class IOConfiguration;

/**
 * Start a run of gabac coding
 * @param conf i/o configuration
 * @param enConf gabac configuration
 * @param decode If you want to decode (true) or encode (false).
 */
void run(
        const IOConfiguration& conf,
        const EncodingConfiguration& enConf,
        bool decode
);
}  // namespace gabac

#endif  // GABAC_RUN_H_
