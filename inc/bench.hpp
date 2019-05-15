#ifndef GRANITE_BENCH_HPP
#define GRANITE_BENCH_HPP
#pragma once

#include <chrono>

namespace granite {
    namespace bench {

        // TODO : Add donotoptimise
        // TODO : Add fast loop
        using d_clock = std::chrono::steady_clock;
        using d_time_point = typename d_clock::time_point;
        using d_duration = typename d_clock::duration;

        template<typename It>
        struct iterator_predicate_t {
            It end;

            iterator_predicate_t(It end):end(end) {}

            bool operator()(It begin) {
                return begin != end;
            }
        };

        template<typename It>
        struct iterator_consumer {
            It output;

            iterator_consumer(It output):output(output) {}

            template<typename Data>
            void operator()(Data data) {
                *output = data;
                ++output;
            }
        };


        template<typename It, typename P, typename C>
        auto bench(It input, P pred, C consumer) {
            while(pred(input)) {
                consume(*input);
                ++input;
            }
            return { input, consume };
        } 


        

        struct steady_timer {
            d_time_point start;

            steady_timer():start(d_clock::now()){}

            std::tuple<d_time_point, d_time_point> operator()() const {
                return { start, d_clock::now() };
            }

        };



        struct State {
            int iter_limit = 100;
            d_duration duration_limit = 5s;

            bool expired(int iter, d_duration d) {
                return iter == iter_limit || d > duration_limit;
            }
        };

        struct bench_iterator {
            using clock_type = d_clock;
            State state;
            int iteration_nb;
            d_time_point begin;

            bench_iterator(State state):
                state(state), iteration_nb(0),
                begin(clock_type::now())
            {}

            State& operator*() {
                return state;
            }

            bench_iterator& operator++() noexcept {
                ++iteration_nb;
                return *this;
            }

            bool end() {
                auto time_spend =
                    bench_iterator::clock_type::now() - begin;

                return state.expired(iteration_nb, begin);
            }
        };

        bool bench_predicate(const bench_iterator& bi) {
            
            
            return bi.state.reach_limit(bi)
        }


        template<>
        struct fun {
            

            void operator()(State& state) {
                auto scoped = scoped_bench(generator, );

                under_fun();


            }
        }




        template<typename G>
        struct scoped_symetric_generator_t {
            using data_type = decltype(std::declval<G&>()());
            
            G generator;
            




        };



        template<typename G, typename It>
        struct bench_guard_t {
            G g;
            It it;
            const auto start = g();

            ~bench_guard_t() {
                const auto stop = g();

                *it = stop - start;
            } 
        };


        template<typename >
        struct BenchIt {


            auto operator()(auto input) {
                auto bg = bench_guard(g, out_it);
                f();

            }
        };
        

        

    }
}

#endif //GRANITE_BENCH_HPP