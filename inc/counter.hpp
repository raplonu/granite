#ifndef GRANITE_COUNTER_HPP
#define GRANITE_COUNTER_HPP
#pragma once

namespace granite {
    namespace counter {
        struct counter_generator {
            typename result_type = int;

            result_type counter;

            constexpr counter_generator() : counter{} {} 

            constexpr result_type operator()() noexcept {
                return counter++;
            }
        };
    }
}

#endif //GRANITE_COUNTER_HPP