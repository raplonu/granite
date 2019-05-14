#ifndef GRANITE_CLOCK_HPP
#define GRANITE_CLOCK_HPP
#pragma once

#include <chrono>
#include <tuple>

namespace granite {
    namespace clock {

        using default_clock = std::chrono::steady_clock;

        // TODO : Add arithmetic capabilities to time_point in order to meet the concept requirement.
        // template<typename... Clocks>
        // struct multi_clock {
        //     using rep =         std::tuple<typename Clocks::rep...>;
        //     using period =      std::tuple<typename Clocks::period...>;
        //     using duration =    std::tuple<typename Clocks::duration...>;
        //     struct time_point : std::tuple<typename Clocks::time_point...> {
        //         using clock = multi_clock;
        //     };

        //     static time_point now() noexcept(noexcept(std::make_tuple(Clocks::now()...))) {
        //         return { std::make_tuple(Clocks::now()...) };
        //     }
        // };

        template<typename Clock>
        struct clock_generator {
            typename clock = Clock;
            typename result_type = typename clock::time_point;

            result_type operator()() const noexcept(noexcept(clock::now())) {
                return clock::now();
            }
        };
    }
}

#endif //GRANITE_CLOCK_HPP